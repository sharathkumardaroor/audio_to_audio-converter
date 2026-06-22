use lofty::prelude::*;
use lofty::probe::Probe;
use lofty::config::WriteOptions;

pub fn copy_metadata(input_path: &str, output_path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let tagged_file = Probe::open(input_path)?.read()?;

    if let Some(tag) = tagged_file.primary_tag() {
        // For the purpose of this conversion, we'll try to save the primary tag.
        tag.save_to_path(output_path, WriteOptions::default())?;
    }

    Ok(())
}
