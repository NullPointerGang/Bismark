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

        const download_response = await fetch('/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: inputValue,
                format: selectValue
            }),
        });
        if (download_response.status == 200) {
            await saveContent(download_response);
        } else {
            alert("Error downloading content");
        }
        }

    } catch (error) {
        console.error('An error occurred:', error);
    } finally {
        button.disabled = false;
        input.readOnly = false;
    }
});

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

async function showInfo(metadata) {
    try {
        const infoElement = document.getElementById("info");

        if (metadata.thumbnail && metadata.title) {
            infoElement.querySelector('img').src = metadata.thumbnail;
            infoElement.querySelector('h1').innerText = metadata.title;
            infoElement.style.display = 'flex';
        } else {
            console.error('Invalid metadata:', metadata);
        }
    } catch (error) {
        console.error('Error displaying info:', error);
    }
}
