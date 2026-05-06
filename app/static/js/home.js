document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("filtros-home").addEventListener("submit", (e) => {
        e.preventDefault();

        const q = document.getElementById("busqueda").value;
        const categoria = document.getElementById("categoria").value;

        let url = "/?";

        if (q) url += `q=${encodeURIComponent(q)}&`;
        if (categoria) url += `categoria=${categoria}`;

        window.location.href = url;
    });

});