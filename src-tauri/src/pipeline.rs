use symphonia::core::audio::AudioBufferRef;
use symphonia::core::codecs::{DecoderOptions, CODEC_TYPE_NULL};
use symphonia::core::errors::Error;
use symphonia::core::formats::FormatOptions;
use symphonia::core::io::MediaSourceStream;
use symphonia::core::meta::MetadataOptions;
use symphonia::core::probe::Hint;
use std::fs::File;
use std::path::Path;
use hound::{WavWriter, WavSpec};
use rubato::{Resampler, FastFixedIn};

pub enum TargetFormat {
    Mp3,
    Wav,
    Flac,
}

pub fn convert_file(input_path: &str, output_path: &str, target_format: TargetFormat) -> Result<(), Box<dyn std::error::Error>> {
    let src = File::open(input_path)?;
    let mss = MediaSourceStream::new(Box::new(src), Default::default());
    let mut hint = Hint::new();
    if let Some(ext) = Path::new(input_path).extension().and_then(|s| s.to_str()) {
        hint.with_extension(ext);
    }

    let format_opts = FormatOptions::default();
    let metadata_opts = MetadataOptions::default();
    let probed = symphonia::default::get_probe().format(&hint, mss, &format_opts, &metadata_opts)?;

    let mut format = probed.format;
    let track = format
        .tracks()
        .iter()
        .find(|t| t.codec_params.codec != CODEC_TYPE_NULL)
        .ok_or("no supported audio track")?;

    let dec_opts = DecoderOptions::default();
    let mut decoder = symphonia::default::get_codecs().make(&track.codec_params, &dec_opts)?;
    let track_id = track.id;

    let mut sample_rate = 0;
    let mut channels = 0;

    let mut all_samples: Vec<Vec<f32>> = Vec::new();

    loop {
        let packet = match format.next_packet() {
            Ok(packet) => packet,
            Err(Error::IoError(ref e)) if e.kind() == std::io::ErrorKind::UnexpectedEof => break,
            Err(e) => return Err(Box::new(e)),
        };

        if packet.track_id() != track_id {
            continue;
        }

        match decoder.decode(&packet) {
            Ok(audio_buf) => {
                let spec = *audio_buf.spec();
                sample_rate = spec.rate;
                let channel_count = spec.channels.count();
                if channels == 0 {
                    channels = channel_count;
                    all_samples = vec![Vec::new(); channels];
                }

                match audio_buf {
                    AudioBufferRef::F32(buf) => {
                        for (i, plane) in buf.planes().planes().iter().enumerate() {
                            all_samples[i].extend_from_slice(plane);
                        }
                    }
                    _ => {
                         let mut temp_buf = audio_buf.make_equivalent::<f32>();
                         audio_buf.convert(&mut temp_buf);
                         for (i, plane) in temp_buf.planes().planes().iter().enumerate() {
                             all_samples[i].extend_from_slice(plane);
                         }
                    }
                }
            }
            Err(Error::DecodeError(_)) => continue,
            Err(e) => return Err(Box::new(e)),
        }
    }

    // Resampling logic (Example: normalize to 44100 if it's not already)
    let target_sample_rate = 44100;
    let mut processed_samples = all_samples;
    if sample_rate != target_sample_rate {
        let mut resampler = FastFixedIn::<f32>::new(
            target_sample_rate as f64 / sample_rate as f64,
            2.0,
            rubato::PolynomialDegree::Septic,
            1024,
            channels,
        )?;
        processed_samples = resampler.process(&processed_samples, None)?;
        sample_rate = target_sample_rate;
    }

    match target_format {
        TargetFormat::Wav => {
            let spec = WavSpec {
                channels: channels as u16,
                sample_rate: sample_rate,
                bits_per_sample: 16,
                sample_format: hound::SampleFormat::Int,
            };
            let mut writer = WavWriter::create(output_path, spec)?;
            let num_samples = processed_samples[0].len();
            for i in 0..num_samples {
                for chan in 0..channels {
                    let sample = processed_samples[chan][i];
                    writer.write_sample((sample * i16::MAX as f32) as i16)?;
                }
            }
            writer.finalize()?;
        }
        _ => {
            // For now, let's just output WAV for everything until we fix the other encoders.
            // But we'll at least use the resampled audio.
            let spec = WavSpec {
                channels: channels as u16,
                sample_rate: sample_rate,
                bits_per_sample: 16,
                sample_format: hound::SampleFormat::Int,
            };
            let mut writer = WavWriter::create(output_path, spec)?;
            let num_samples = processed_samples[0].len();
            for i in 0..num_samples {
                for chan in 0..channels {
                    let sample = processed_samples[chan][i];
                    writer.write_sample((sample * i16::MAX as f32) as i16)?;
                }
            }
            writer.finalize()?;
        }
    }

    Ok(())
}
