console.log("Funciona")
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("form-valorar").addEventListener("submit", async (e) => {
        e.preventDefault();

        const producto_id = document.getElementById("producto_id").value;
        const vendedor_id = document.getElementById("vendedor_id").value;
        const puntuacion = document.getElementById("puntuacion").value;
        const comentario = document.getElementById("comentario").value;

        try {
            const res = await fetch(`/valorar/${vendedor_id}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    producto_id,
                    puntuacion,
                    comentario
                })
            });

            if (res.ok) {
                const opiniones = document.querySelector(".opiniones");
                const nueva = document.createElement("div");
                nueva.classList.add("opinion");
                nueva.innerHTML = `
                    <strong>${puntuacion} ⭐</strong>
                    <p>${comentario}</p>
                `;
                opiniones.prepend(nueva);
                document.getElementById("comentario").value = "";
                document.getElementById("resultado").innerText = "Valoración enviada";

            } else {
                const result = await res.json();
                document.getElementById("resultado").innerText =
                    result.error || "Error";
            }

        } catch (error) {
            document.getElementById("resultado").innerText = "Error conexión";
        }
    });

});