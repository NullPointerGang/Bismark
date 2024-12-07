document.getElementById("submit-button").addEventListener('click', async () => {
    const inputValue = document.getElementById("url-input").value;
    const selectValue = document.getElementById("select-format").value;

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
    } else {
        console.error('Download failed');
    }
})
