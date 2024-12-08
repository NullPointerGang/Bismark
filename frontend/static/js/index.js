document.getElementById("submit-button").addEventListener('click', async () => {
    const input = document.getElementById("url-input");
    const selectValue = document.getElementById("select-format").value;
    const button = document.getElementById("submit-button");

    const inputValue = input.value;
    if (!inputValue || !selectValue) return;

    button.disabled = true;
    input.readOnly = true;

    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: inputValue,
                format: selectValue
            }),
        });

        if (response.ok) {
            const metadata = await response.clone().json();
            await showInfo(metadata);
            
            await saveContent(response, selectValue);
        } else {
            console.error('Download failed:', await response.text());
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

        if (metadata.thumbnail && metadata.title) {
            infoElement.querySelector('img').src = metadata.thumbnail;
            infoElement.querySelector('h1').innerText = metadata.title;
            infoElement.style.display = 'block';
        } else {
            console.error('Invalid metadata:', metadata);
        }
    } catch (error) {
        console.error('Error displaying info:', error);
    }
}
