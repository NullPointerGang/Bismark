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

    const data = await response.json();

    console.log(data)
})
