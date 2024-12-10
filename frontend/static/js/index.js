document.getElementById("submit-button").addEventListener('click', async () => {
    const input = document.getElementById("url-input");
    const button = document.getElementById("submit-button");

    const inputValue = input.value;
    if (!inputValue) return;

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

async function showInfo(metadata) {
    try {
        const infoElement = document.getElementById("info");
        const imageElement = document.getElementById("video-thumbnail");
        const textElement = document.getElementById("video-title");
        if (metadata.thumbnail && metadata.title) {
            console.log("Metadata:", metadata);
            await buttonsGenerator(metadata);
            console.log("Buttons generated");
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

async function buttonsGenerator(metadata) {
    const container = document.getElementById("button-container");
    container.innerHTML = '';

    const qualityList = metadata.quality_list;
    if (!qualityList) {
        console.error("No quality_list found in metadata.");
        return;
    }
    const buttonNames = {
        "audio_only": "Download Audio",
        "video_only": "Download Video",
        "max_quality": "Download Max Quality",
    }
    for (const [key, format] of Object.entries(qualityList)) {
        const input = document.getElementById("url-input");
        const button = document.createElement("button");
        button.innerText = format.label || buttonNames[key];
        button.addEventListener('click', async () => {
            try {
                const response = await fetch('/download', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        url: input.value,
                        format_id: format.format_id,
                    }),
                });

                if (response.status === 200) {
                    await saveContent(response);
                } else {
                    console.error(`Failed to download ${key}:`, response.statusText);
                }
            } catch (error) {
                console.error(`Error downloading ${key}:`, error);
            }
        });

        container.appendChild(button);
    }
}


async function saveContent(response) {
    try {
        const json = await response.json();
        const fileUrl = json.file_url;
        const a = document.createElement("a");
        a.href = fileUrl;
        a.click();
    } catch (error) {
        console.error('Error saving content:', error);
    }
}


