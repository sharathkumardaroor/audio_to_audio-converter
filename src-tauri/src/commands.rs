use serde::{Deserialize, Serialize};
use crate::pipeline::{convert_file, TargetFormat};
use crate::metadata::copy_metadata;
use std::path::Path;
use rayon::prelude::*;

#[derive(Serialize, Deserialize)]
pub struct ConversionResult {
    pub success: bool,
    pub message: String,
    pub file: String,
}

#[tauri::command]
pub fn start_conversion(
    files: Vec<String>,
    output_folder: String,
    target_format: String,
) -> Vec<ConversionResult> {
    files.into_par_iter().map(|file_path| {
        let path = Path::new(&file_path);
        let file_name = path.file_stem().unwrap().to_str().unwrap();
        let out_path = Path::new(&output_folder).join(format!("{}.{}", file_name, target_format));
        let out_path_str = out_path.to_str().unwrap();

        let format = match target_format.as_str() {
            "mp3" => TargetFormat::Mp3,
            "wav" => TargetFormat::Wav,
            "flac" => TargetFormat::Flac,
            _ => TargetFormat::Wav,
        };

        match convert_file(&file_path, out_path_str, format) {
            Ok(_) => {
                // Try to copy metadata
                let _ = copy_metadata(&file_path, out_path_str);
                ConversionResult {
                    success: true,
                    message: "Success".to_string(),
                    file: file_path,
                }
            },
            Err(e) => ConversionResult {
                success: false,
                message: e.to_string(),
                file: file_path,
            }
        }
    }).collect()
}
