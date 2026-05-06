document.addEventListener("DOMContentLoaded", function () {

    const container = document.getElementById("paypal-button-container");

    if (!container) return;

    const productoId = container.dataset.productoId;
    const precio = container.dataset.precio;

    console.log("Producto:", productoId);
    console.log("Precio:", precio);

    paypal.Buttons({

        createOrder: function (data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: precio.toString()
                    }
                }]
            });
        },

        onApprove: function (data, actions) {
            return actions.order.capture().then(function (details) {

                console.log("Pago OK:", details);

                fetch("/api/compra", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        producto_id: productoId,
                        paypal_order_id: data.orderID,
                        status: "completed"
                    })
                });

                alert("Pago completado");
            });
        },

        onError: function (err) {
            console.error("ERROR PAYPAL:", err);
        },

        onCancel: function () {
            console.log("Cancelado");
        }

    }).render("#paypal-button-container");

});