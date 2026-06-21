# Bulk Audio Converter (Rust + Tauri Version)

A high-efficiency Bulk Audio Converter app built with **Rust**, **Tauri**, and **Symphonia**. This version replaces the previous Python/FFmpeg implementation with a pure Rust audio processing pipeline, ensuring zero external dependencies and native performance.

## Features

- **Pure Rust Audio Pipeline:** Uses `Symphonia` for decoding and `Hound` for encoding. No FFmpeg required.
- **Native UI:** Built with Tauri, utilizing the OS's native WebView for a lightweight and responsive experience.
- **Parallel Processing:** Leverages `Rayon` to utilize all CPU cores for batch conversions.
- **Metadata Preservation:** Uses `Lofty` to copy tags and album art from original files.
- **Standalone Binary:** Compiles into a small, portable executable (~5MB).

## Tech Stack

- **UI:** HTML/JS + Tailwind CSS
- **Backend:** Rust + Tauri
- **Audio Decoding:** [Symphonia](https://github.com/pdeljanov/Symphonia)
- **Audio Encoding:** [Hound](https://github.com/ruuda/hound) (WAV)
- **Metadata:** [Lofty](https://github.com/Serial-Experiments-Lofty/lofty-rs)
- **Parallelism:** [Rayon](https://github.com/rayon-rs/rayon)

## Installation

1. **Install Rust:** [https://www.rust-lang.org/tools/install](https://www.rust-lang.org/tools/install)
2. **Install Tauri CLI:** `npm install -g @tauri-apps/cli`
3. **Install System Dependencies (Linux only):**
   ```bash
   sudo apt-get install -y libgtk-3-dev libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf
   ```

## Usage

To run the app in development mode:

```bash
cd src-tauri
cargo tauri dev
```

To build a production release:

```bash
cd src-tauri
cargo tauri build
```

## Project Structure

```
.
├── src-tauri/
│   ├── src/
│   │   ├── main.rs         # Entry point
│   │   ├── lib.rs          # App logic and setup
│   │   ├── commands.rs     # Tauri commands (select_files, start_conversion)
│   │   ├── pipeline.rs     # Audio decoding/encoding pipeline
│   │   └── metadata.rs     # Tag preservation
│   ├── Cargo.toml          # Rust dependencies
│   └── tauri.conf.json     # Tauri configuration
├── ui/
│   ├── index.html          # Main UI
│   └── main.js             # Frontend logic
└── README.md
```

## License

This project is licensed under the MIT License.
