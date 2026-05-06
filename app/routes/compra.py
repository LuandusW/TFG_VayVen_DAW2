from flask import Blueprint, request, jsonify, session
from sqlalchemy import text

from app import db
from app.paypal_cliente import paypal_client

from paypalcheckoutsdk.orders import OrdersCaptureRequest


compras_bp = Blueprint("compras", __name__)


@compras_bp.route("/crear-venta", methods=["POST"])
def crear_venta():

    user_id = session.get("user_id")

    if not user_id:
        return jsonify({
            "success": False,
            "error": "No autenticado"
        }), 401

    data = request.get_json()

    producto_id = data.get("producto_id")
    paypal_order_id = data.get("paypal_order_id")
    amount = data.get("amount")

    if not producto_id or not paypal_order_id or not amount:
        return jsonify({
            "success": False,
            "error": "Datos incompletos"
        }), 400

    try:

        capture_request = OrdersCaptureRequest(paypal_order_id)

        capture = paypal_client.execute(capture_request)

        status = capture.result.status

        if status != "COMPLETED":
            return jsonify({
                "success": False,
                "error": "Pago no completado"
            }), 400

        payer_email = capture.result.payer.email_address

        producto = db.session.execute(text("""
            SELECT vendedor_id, precio
            FROM productos
            WHERE id = :id
        """), {
            "id": producto_id
        }).fetchone()

        if not producto:
            return jsonify({
                "success": False,
                "error": "Producto no existe"
            }), 404

        vendedor_id = producto[0]
        precio_real = float(producto[1])

        if vendedor_id == user_id:
            return jsonify({
                "success": False,
                "error": "No puedes comprar tu propio producto"
            }), 400

        if float(amount) != precio_real:
            return jsonify({
                "success": False,
                "error": "Precio manipulado"
            }), 400

        venta_existente = db.session.execute(text("""
            SELECT id
            FROM ventas
            WHERE producto_id = :id
        """), {
            "id": producto_id
        }).fetchone()

        if venta_existente:
            return jsonify({
                "success": False,
                "error": "Producto ya vendido"
            }), 400

        venta = db.session.execute(text("""
            INSERT INTO ventas (
                comprador_id,
                producto_id,
                precio,
                estado
            )
            VALUES (
                :comprador_id,
                :producto_id,
                :precio,
                'pagado'
            )
            RETURNING id
        """), {
            "comprador_id": user_id,
            "producto_id": producto_id,
            "precio": precio_real
        }).fetchone()

        venta_id = venta[0]

        db.session.execute(text("""
            INSERT INTO pagos (
                venta_id,
                paypal_order_id,
                payer_email,
                amount,
                status
            )
            VALUES (
                :venta_id,
                :paypal_order_id,
                :payer_email,
                :amount,
                'completed'
            )
        """), {
            "venta_id": venta_id,
            "paypal_order_id": paypal_order_id,
            "payer_email": payer_email,
            "amount": precio_real
        })

        db.session.commit()

        return jsonify({
            "success": True,
            "venta_id": venta_id
        })

    except Exception as e:

        db.session.rollback()

        import traceback
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500