const { invoke } = window.__TAURI__.core;
const { open } = window.__TAURI__.dialog;

let selectedFiles = [];
let outputFolder = "";

const selectFilesBtn = document.getElementById('select-files');
const selectFolderBtn = document.getElementById('select-folder');
const startBtn = document.getElementById('start-conversion');
const fileCountText = document.getElementById('file-count');
const folderPathText = document.getElementById('folder-path');
const formatSelect = document.getElementById('format');
const progressContainer = document.getElementById('progress-container');
const progressBar = document.getElementById('progress-bar');
const progressText = document.getElementById('progress-text');
const statusDiv = document.getElementById('status');

selectFilesBtn.addEventListener('click', async () => {
    const selected = await open({
        multiple: true,
        filters: [{
            name: 'Audio',
            extensions: ['wav', 'mp3', 'flac', 'ogg', 'm4a']
        }]
    });
    if (selected) {
        selectedFiles = Array.isArray(selected) ? selected : [selected];
        fileCountText.textContent = `${selectedFiles.length} file(s) selected`;
        updateStartButton();
    }
});

selectFolderBtn.addEventListener('click', async () => {
    const selected = await open({
        directory: true,
    });
    if (selected) {
        outputFolder = selected;
        folderPathText.textContent = `Output: ${outputFolder}`;
        updateStartButton();
    }
});

function updateStartButton() {
    startBtn.disabled = !(selectedFiles.length > 0 && outputFolder !== "");
}

startBtn.addEventListener('click', async () => {
    statusDiv.textContent = "Converting...";
    progressContainer.classList.remove('hidden');
    startBtn.disabled = true;

    try {
        const results = await invoke('start_conversion', {
            files: selectedFiles,
            outputFolder: outputFolder,
            targetFormat: formatSelect.value
        });

        const successCount = results.filter(r => r.success).length;
        statusDiv.textContent = `Completed: ${successCount}/${selectedFiles.length} successful.`;

        // Update progress to 100%
        progressBar.style.width = '100%';
        progressText.textContent = `${selectedFiles.length}/${selectedFiles.length}`;

    } catch (error) {
        statusDiv.textContent = `Error: ${error}`;
    } finally {
        startBtn.disabled = false;
    }
});
