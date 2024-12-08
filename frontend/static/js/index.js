document.getElementById("submit-button").addEventListener('click', async () => {
    const input = document.getElementById("url-input");
    const selectValue = document.getElementById("select-format").value;

    const inputValue = input.value;

    if (!inputValue) return;
    if (!selectValue) return;



    const button = document.getElementById("submit-button")

    button.disabled = true;

    input.readOnly = true;

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
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        if (selectValue === 'mp3') {
            a.download = 'audio.mp3';
        } else {
            a.download = 'video.mp4';
        }
        a.click();
        const info_element = document.getElementById("info");

        const info = await response.json();
        const thumbnail = info.thumbnail;
        const title = info.title;

        info_element.getElementsByTagName('img')[0].src = thumbnail;
        info_element.getElementsByTagName('h1')[0].innerText = title;
        info_element.style.display = 'block';
        

    } else {
        console.error('Download failed');
    }
    button.disabled = false;
    input.readOnly = false;
})
