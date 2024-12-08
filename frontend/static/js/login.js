document.getElementById("submit").addEventListener("click", async () => {
    const usernameInput = document.getElementById("username")
    const passwordInput = document.getElementById("password")

    const username = usernameInput.value
    const password = passwordInput.value

    if (!username) return;
    if (!password) return;

    const button = document.getElementById("submit")

    button.disabled = true;
    usernameInput.readOnly = true;
    passwordInput.readOnly = true;

    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: btoa(username),
            password: btoa(password)
        }),
    });

    if (response.status == 200){
        // Loged in
        alert("Login successed")
        window.location.href('/')
    } else if (response.status == 401) {
        // Not loged in
        alert("Ti loh")
    }
})
