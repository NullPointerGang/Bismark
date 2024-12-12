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
            await buttonsGenerator(metadata);
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

    const qualityList = metadata.video_formats;
    if (!qualityList) {
        console.error("No quality_list found in metadata.");
        return;
    }

    const table = document.createElement("table")
    container.appendChild(table)

    for (const [key, format] of Object.entries(qualityList)) {
        const input = document.getElementById("url-input");

        const filesize = bToMb(format.filesize)

        const tr = document.createElement("tr");
        table.appendChild(tr);

        const tdResolution = document.createElement("td");
        tdResolution.innerText = format.resolution || "Unknown Resolution";
        tr.appendChild(tdResolution);

        const tdButton = document.createElement("td");
        tdButton.innerHTML = `<button class="download-button" onclick="startDownload('${input.value}', ${format.format_id})">Download</button>`

        tr.appendChild(tdButton);
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


async function startDownload(url, format_id) {
    const buttons = document.getElementsByClassName("download-button");
    for (const button of buttons) {
        button.disabled = true;
    }
    try {
        const response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                format_id: format_id,
            }),
        });

        if (response.status === 200) {
            await saveContent(response);
        } else {
            console.error(`Failed to download `, response.statusText);
        }
    } catch (error) {
        console.error(`Error downloading `, error);
    }
    for (const button of buttons) {
        button.disabled = false;
    }
}


function bToMb(b) {
    return (b / 1024 / 1024).toFixed(2);
}
