document.getElementById("form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const password = document.getElementById("password").value;

    try {
        const res = await fetch(`/reset/${token}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ password })
        });

        const result = await res.json();

        if (res.ok) {
            document.getElementById("resultado").innerText = result.msg;
            setTimeout(() => {
                window.location.href = "/login";
            }, 2000);
        } else {
            document.getElementById("resultado").innerText = result.error;
        }

    } catch (error) {
        document.getElementById("resultado").innerText =
            "Error al conectar con el servidor";
    }
});