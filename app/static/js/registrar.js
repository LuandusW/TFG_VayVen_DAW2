console.log("JS")
document.getElementById("form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
        nombre: document.getElementById("nombre").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value
    };

    const res = await fetch("/registrar", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    if (res.ok) {
        setTimeout(() => {
            window.location.href = "/";
        }, 1500);

    } else {
        document.getElementById("resultado").innerText = result.error;
    }
});