console.log("asdhuasdhu")
document.getElementById("form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const res = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password })
        });

        const result = await res.json();

        if (res.ok) {
            setTimeout(() => {
                window.location.href = "/";
            }, 1500);

        } else {
            document.getElementById("resultado").innerText = result.error;
        }

    } catch (error) {
        document.getElementById("resultado").innerText =
            "Error al conectar con el servidor";
    }
});