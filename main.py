
import os
import ffmpeg
import threading
import flet as ft

# Set path to FFmpeg executable (update if necessary)
FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"
if not os.path.isfile(FFMPEG_PATH):
    raise FileNotFoundError(f"FFmpeg not found at {FFMPEG_PATH}. Please install FFmpeg and update FFMPEG_PATH accordingly.")

def main(page: ft.Page):
    page.title = "Bulk Audio Converter"
    page.bgcolor = ft.Colors.WHITE
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Global variables for selected files, output folder, and conversion results.
    selected_files = []
    output_folder = None
    successes = []
    errors = []

    # UI Controls
    file_list_text = ft.Text("No files selected", color=ft.Colors.BLACK, size=12)
    output_folder_text = ft.Text("No output folder selected", color=ft.Colors.BLACK, size=12)
    current_file_text = ft.Text("Processing: None", color=ft.Colors.BLACK, size=12)
    progress_text = ft.Text("", color=ft.Colors.BLACK, size=12)
    progress_bar = ft.ProgressBar(width=180)
    format_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("mp3"),
            ft.dropdown.Option("wav"),
            ft.dropdown.Option("ogg"),
            ft.dropdown.Option("flac"),
            ft.dropdown.Option("m4a")
        ],
        value="mp3",
        width=100,
        
    )

    # FilePicker for selecting input files.
    def files_picked(e: ft.FilePickerResultEvent):
        nonlocal selected_files
        if e.files:
            selected_files = [f.path for f in e.files]
            file_list_text.value = f"{len(selected_files)} file(s) selected."
        else:
            file_list_text.value = "No files selected."
        page.update()

    file_picker = ft.FilePicker(on_result=files_picked)
    page.overlay.append(file_picker)

    # FilePicker for selecting a folder via directory path.
    def folder_picked(e: ft.FilePickerResultEvent):
        nonlocal output_folder
        if e.path:
            output_folder = e.path
            output_folder_text.value = f"Output Folder: {output_folder}"
        else:
            output_folder_text.value = "No output folder selected."
        page.update()

    folder_picker = ft.FilePicker(on_result=folder_picked)
    page.overlay.append(folder_picker)

    # Conversion function running in a separate thread.
    def convert_bulk():
        nonlocal successes, errors
        successes = []
        errors = []
        if output_folder is None:
            errors.append("No output folder selected.")
            return

        os.makedirs(output_folder, exist_ok=True)
        total = len(selected_files)
        progress_bar.value = 0
        page.update()

        for idx, file in enumerate(selected_files):
            current_file_text.value = f"Processing: {os.path.basename(file)}"
            page.update()
            if not os.path.isfile(file):
                errors.append(f"File not found: {file}")
                progress_bar.value = (idx + 1) / total
                progress_text.value = f"{idx + 1}/{total}"
                page.update()
                continue

            target_format = format_dropdown.value
            base_name = os.path.splitext(os.path.basename(file))[0]
            output_file = os.path.join(output_folder, f"{base_name}.{target_format}")

            try:
                ffmpeg.input(file).output(
                    output_file, format=target_format, audio_bitrate="192k"
                ).run(cmd=FFMPEG_PATH, quiet=True, overwrite_output=True)
                successes.append(f"Converted: {file} -> {output_file}")
            except ffmpeg.Error as e:
                err = e.stderr.decode() if e.stderr else str(e)
                errors.append(f"Error converting {file}: {err}")
            except Exception as ex:
                errors.append(f"Error converting {file}: {str(ex)}")

            progress_bar.value = (idx + 1) / total
            progress_text.value = f"{idx + 1}/{total}"
            page.update()

        summary = (
            f"Total Files: {total}\n"
            f"Success: {len(successes)}\n"
            f"Errors: {len(errors)}\n\n"
            f"Successes:\n" + "\n".join(successes) +
            "\n\nErrors:\n" + "\n".join(errors)
        )
        dlg = ft.AlertDialog(
            title=ft.Text("Summary", color=ft.Colors.BLACK),
            content=ft.Text(summary, color=ft.Colors.BLACK, size=12),
            actions=[ft.TextButton("Close", on_click=lambda e: close_dialog())],
        )
        page.dialog = dlg
        dlg.open = True
        page.update()
        current_file_text.value = "Processing: None"
        page.update()

    def close_dialog():
        page.dialog.open = False
        page.update()

    def start_conversion(e):
        if not selected_files or output_folder is None:
            page.show_snack_bar(ft.SnackBar(ft.Text("Select files and output folder first!", size=12)))
            return
        threading.Thread(target=convert_bulk, daemon=True).start()

    # Create buttons with custom text content for styling.
    pick_files_button = ft.ElevatedButton(
        content=ft.Text("Select Files", size=12),
        bgcolor=ft.Colors.LIGHT_BLUE,
        color=ft.Colors.BLACK,
        on_click=lambda e: file_picker.pick_files(allow_multiple=True),
        width=90,
        height=30
    )
    pick_folder_button = ft.ElevatedButton(
        content=ft.Text("Output Folder", size=10),
        bgcolor=ft.Colors.LIGHT_BLUE,
        color=ft.Colors.BLACK,
        on_click=lambda e: folder_picker.get_directory_path(dialog_title="Select Output Folder"),
        width=90,
        height=30
    )
    start_button = ft.ElevatedButton(
        content=ft.Text("Start Conversion", size=12),
        bgcolor=ft.Colors.LIGHT_BLUE,
        color=ft.Colors.BLACK,
        on_click=start_conversion,
        width=130,
        height=30
    )

    # Layout using 1, 3, 2 columns

    # Row 1: Single column for the title
    row1 = ft.Row(
        controls=[
            ft.Container(content=ft.Text("Bulk Audio Converter", size=18, weight="bold", color=ft.Colors.BLACK), expand=True, alignment=ft.alignment.center)
        ]
    )

    # Row 2: Three columns
    col_file = ft.Column(
        controls=[pick_files_button, file_list_text],
        spacing=3,
        alignment=ft.MainAxisAlignment.CENTER
    )
    col_folder = ft.Column(
        controls=[pick_folder_button, output_folder_text],
        spacing=3,
        alignment=ft.MainAxisAlignment.CENTER
    )
    col_format = ft.Column(
        controls=[ft.Text("Format:", size=10, color=ft.Colors.BLACK), format_dropdown],
        spacing=3,
        alignment=ft.MainAxisAlignment.CENTER
    )
    row2 = ft.Row(
        controls=[col_file, col_folder, col_format],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Row 3: Two columns
    col_status = ft.Column(
        controls=[current_file_text, progress_bar, progress_text],
        spacing=3,
        alignment=ft.MainAxisAlignment.CENTER
    )
    row3 = ft.Row(
        controls=[col_status, ft.Container(content=start_button, alignment=ft.alignment.center)],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Add rows to the main column layout with a reduced overall width
    page.add(
        ft.Column(
            controls=[row1, row2, row3],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=300
        )
    )

ft.app(target=main)
