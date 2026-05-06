console.log("hola")
document.addEventListener("DOMContentLoaded", () => {


    document.getElementById("form-publicar").addEventListener("submit", async (e) => {
        e.preventDefault();

        const titulo = document.getElementById("titulo").value;
        const descripcion = document.getElementById("descripcion").value;
        const precio = document.getElementById("precio").value;
        const categoria = document.getElementById("categoria").value;
        const foto_url = document.getElementById("foto_url").value.trim();

        const resultado = document.getElementById("resultado");
        try {
            new URL(foto_url);
        } catch {
            resultado.innerText = "URL no válida";
            return;
        }

        const extensiones = [".jpg", ".jpeg", ".png", ".webp", ".gif"];

        const esImagen = extensiones.some(ext => 
            foto_url.toLowerCase().includes(ext)
        );

        if (!esImagen) {
            resultado.innerText = "La URL no es una imagen válida";
            return;
        }

        const data = {
            titulo,
            descripcion,
            precio,
            categoria_id: categoria,
            foto_url
        };

        try {
            const res = await fetch("/publicar", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            if (res.ok) {
                window.location.href = "/";
            } else {
                const result = await res.json();
                resultado.innerText = result.error || "Error al publicar";
            }

        } catch (error) {
            resultado.innerText = "Error de conexión";
        }
    });

});