```
README.md
# Bulk Audio Converter

A simple Bulk Audio Converter app built using [Flet](https://flet.dev/) and [FFmpeg](https://ffmpeg.org/). This application lets you select multiple audio files, choose an output folder, and convert the files to a target format (e.g., mp3, wav, ogg, flac, m4a) in bulk.

## Features

- **Multi-file Selection:** Choose multiple audio files for conversion.
- **Output Folder Selection:** Specify the folder where the converted files will be saved.
- **Format Options:** Convert audio files to various formats.
- **Progress Tracking:** View the current processing file, progress bar, and progress count.
- **Result Summary:** Displays a summary of successful conversions and errors after the process completes.

## Requirements

- **Python 3.11+** (Tested with Python 3.13)
- [Flet](https://github.com/flet-dev/flet) for the GUI.
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) for interfacing with FFmpeg.
- **FFmpeg** executable installed on your system. Update the `FFMPEG_PATH` in `app/main.py` if needed.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/bulk-audio-converter.git
   ```

2. **Navigate to the project directory:**
   ```bash
   cd bulk-audio-converter
   ```

3. **(Optional) Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install the required packages:**
   ```bash
   pip install flet ffmpeg-python
   ```

5. **Ensure FFmpeg is installed:**
   - Download FFmpeg from [here](https://ffmpeg.org/download.html) if it's not installed.
   - Update the `FFMPEG_PATH` in `app/main.py` to point to the FFmpeg executable if necessary.

## Usage

To run the application, execute:

```bash
python app/main.py
```

- The app will launch in a window sized 200x500.
- **Row 1:** Displays the app title.
- **Row 2:** Contains three columns for file selection, folder selection, and format selection.
- **Row 3:** Contains two columns for status display and the "Start Conversion" button.
- Follow the on-screen prompts:
  - Click **Select Files** to choose audio files.
  - Click **Output Folder** to select a destination folder.
  - Choose the desired format from the dropdown.
  - Click **Start Conversion** to begin processing.
- A summary dialog will appear with conversion details upon completion.

## Project Structure

```
bulk-audio-converter/
│
├── app/
│   └── main.py       # Main application code
├── README.md         # This file
└── requirements.txt  # (Optional) List of dependencies
```

## Version Control & Future Enhancements

- **Version Control:**  
  This project is managed using Git. Commit and tag a new release only after verifying that the current version runs without errors.
  
- **Planned Enhancements:**
  - Additional audio format support.
  - Improved error handling and reporting.
  - UI/UX improvements.
  - Integration with cloud storage services for file management.
  - Batch processing optimizations.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Flet](https://flet.dev/) for the intuitive UI framework.
- [FFmpeg](https://ffmpeg.org/) for robust audio conversion capabilities.
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python) for the Python interface to FFmpeg.
```
