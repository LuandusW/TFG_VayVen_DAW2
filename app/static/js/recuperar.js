
document.getElementById("form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;

    try {
        const res = await fetch("/recuperar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email })
        });

        const result = await res.json();

        document.getElementById("resultado").innerText =
            result.msg || result.error;

    } catch (error) {
        document.getElementById("resultado").innerText =
            "Error al conectar con el servidor";
    }
});