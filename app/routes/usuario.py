from flask import Blueprint, render_template, session, redirect, url_for
from sqlalchemy import text

from app import db
perfil_bp = Blueprint("perfil", __name__)
@perfil_bp.route("/perfil")
def perfil():

    user_id = session.get("user_id")

    if not user_id:
        return redirect(url_for("auth.login_page"))

    usuario = db.session.execute(text("""
        SELECT id, nombre, email, rol, creacion
        FROM usuarios
        WHERE id = :id
    """), {
        "id": user_id
    }).fetchone()

    productos = db.session.execute(text("""
        SELECT id, titulo, precio, creacion
        FROM productos
        WHERE vendedor_id = :id
        ORDER BY creacion DESC
    """), {
        "id": user_id
    }).fetchall()

    compras = db.session.execute(text("""
        SELECT
            ventas.id,
            productos.titulo,
            ventas.precio,
            ventas.estado,
            ventas.creacion
        FROM ventas
        JOIN productos
            ON productos.id = ventas.producto_id
        WHERE ventas.comprador_id = :id
        ORDER BY ventas.creacion DESC
    """), {
        "id": user_id
    }).fetchall()

    return render_template(
        "perfil.html",
        usuario=usuario,
        productos=productos,
        compras=compras
    )