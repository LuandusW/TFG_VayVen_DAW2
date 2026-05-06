from flask import Blueprint, request, render_template, redirect, url_for, session
from app import db
from sqlalchemy import func
from app.models import Producto, Categoria,Valoracion

productos_bp = Blueprint("productos", __name__)


@productos_bp.route("/")
def home():

    query = Producto.query

    busqueda = request.args.get("q")
    if busqueda:
        query = query.filter(Producto.titulo.ilike(f"%{busqueda}%"))

    categoria_id = request.args.get("categoria")
    if categoria_id:
        query = query.filter(Producto.categoria_id == categoria_id)

    productos = query.order_by(Producto.creacion.desc()).all()

    categorias = Categoria.query.all()

    return render_template(
        "home.html",
        productos=productos,
        categorias=categorias
    )


@productos_bp.route("/publicar", methods=["GET", "POST"])
def publicar():

    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    if request.method == "POST":

        data = request.get_json()

        producto = Producto(
            vendedor_id=session["user_id"],
            titulo=data["titulo"],
            descripcion=data.get("descripcion"),
            precio=float(data["precio"]),
            categoria_id=int(data.get("categoria_id")),
            foto_url=data.get("foto_url"),
        )

        db.session.add(producto)
        db.session.commit()

        return {"msg": "ok"}

    categorias = Categoria.query.all()
    return render_template("publicar.html", categorias=categorias)

@productos_bp.route("/producto/<int:id>")
def detalle_producto(id):

    producto = Producto.query.get_or_404(id)

    media = db.session.query(func.avg(Valoracion.puntuacion))\
        .filter_by(destinatario_id=producto.vendedor_id)\
        .scalar()

    valoraciones = Valoracion.query\
        .filter_by(destinatario_id=producto.vendedor_id)\
        .all()

    return render_template("producto.html",producto=producto,media=media,valoraciones=valoraciones
    )

@productos_bp.route("/valorar/<int:vendedor_id>", methods=["POST"])
def valorar(vendedor_id):

    if "user_id" not in session:
        return {"error": "No autorizado"}, 401

    if session["user_id"] == vendedor_id:
        return {"error": "No puedes valorarte"}, 400

    data = request.get_json()

    puntuacion = int(data.get("puntuacion"))
    comentario = data.get("comentario")

    existe = Valoracion.query.filter_by(
        autor_id=session["user_id"],
        destinatario_id=vendedor_id
    ).first()

    if existe:
        return {"error": "Ya has valorado a este vendedor"}, 400

    valoracion = Valoracion(
        autor_id=session["user_id"],
        destinatario_id=vendedor_id,
        puntuacion=puntuacion,
        comentario=comentario
    )

    db.session.add(valoracion)
    db.session.commit()

    return {"msg": "ok"}