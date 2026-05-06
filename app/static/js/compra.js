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

        onApprove: async function (data) {

            console.log("ORDER ID:", data.orderID);

            try {

                const response = await fetch("/crear-venta", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        producto_id: productoId,
                        paypal_order_id: data.orderID,
                        amount: precio
                    })
                });

                const result = await response.json();

                console.log("RESULT:", result);

                if (result.success) {
                    alert("Pago completado");
                } else {
                    alert("Error en el pago");
                }

            } catch (error) {
                console.error(error);
            }
        },

        onError: function (err) {
            console.error("ERROR PAYPAL:", err);
        },

        onCancel: function () {
            console.log("Cancelado");
        }

    }).render("#paypal-button-container");

});