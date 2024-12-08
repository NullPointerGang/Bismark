document.getElementById("submit-button").addEventListener('click', async () => {
    const input = document.getElementById("url-input");
    const selectValue = document.getElementById("select-format").value;
    const button = document.getElementById("submit-button");

    const inputValue = input.value;
    if (!inputValue || !selectValue) return;

    button.disabled = true;
    input.readOnly = true;

    try {
        const info_response = await fetch('/download/info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: inputValue,
            }),
        });

        if (info_response.status == 200) {
            const metadata = await info_response.json();
            await showInfo(metadata);
        }

    } catch (error) {
        console.error('An error occurred:', error);
    } finally {
        button.disabled = false;
        input.readOnly = false;
    }
});

document.getElementById("download-button").addEventListener('click', async () => {
    const input = document.getElementById("url-input");
    const selectValue = document.getElementById("select-format").value;
    const button = document.getElementById("download-button");

    const inputValue = input.value;
    if (!inputValue || !selectValue) return;

    button.disabled = true;
    input.readOnly = true;

    try {
        const download_response = await fetch('/download/file', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                file_path: inputValue,
            }),
        });
        if (download_response.status == 200) {
            await saveContent(download_response, selectValue);
        } else {
            alert("Error downloading content");
        }

    } catch (error) {
        console.error('An error occurred:', error);
    } finally {
        button.disabled = false;
        input.readOnly = false;
    }
});

async function saveContent(response, fileType) {
    try {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = fileType === 'mp3' ? 'audio.mp3' : 'video.mp4';
        a.click();
        window.URL.revokeObjectURL(url);
    } catch (error) {
        console.error('Error saving content:', error);
    }
}

async function showInfo(metadata) {
    try {
        const infoElement = document.getElementById("info");
        const imageElement = document.getElementById("video-thumbnail");
        const textElement = document.getElementById("video-title");
        const buttonElemtn = document.getElementById("download-button");

        if (metadata.thumbnail && metadata.title) {
            imageElement.src = metadata.thumbnail;
            textElement.innerText = metadata.title;
            infoElement.style.display = 'flex';
        } else {
            console.error('Invalid metadata:', metadata);
        }
    } catch (error) {
        console.error('Error displaying info:', error);
    }
}
