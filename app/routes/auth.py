from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models import Usuario, ContrasenaReset
from flask_mail import Message
from app import mail
import bcrypt
from flask import current_app
from flask import session
from flask_mail import Message
from app import mail
from flask import session, redirect, url_for
import os

auth_bp = Blueprint("auth", __name__)


# GET → muestrar formulario
@auth_bp.route("/registrar", methods=["GET"])
def register_page():
    return render_template("registrar.html")


# POST → crear usuario
@auth_bp.route("/registrar", methods=["POST"])
def register():
    data = request.json

    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    if not data.get("nombre") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Faltan campos"}), 400

    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email ya registrado"}), 400

    hashed = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())

    user = Usuario(
        nombre=data["nombre"], email=data["email"], password_hash=hashed.decode()
    )

    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"error": "Error al guardar usuario"}), 500

    return jsonify(
        {
            "msg": "Usuario creado correctamente",
            "user": {"id": user.id, "nombre": user.nombre, "email": user.email},
        }
    ), 201


@auth_bp.route("/recuperar", methods=["GET"])
def recuperar_page():
    return render_template("recuperar.html")


# Enviar Correo
@auth_bp.route("/recuperar", methods=["POST"])
def recuperar():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    email = data.get("email")

    if not email:
        return jsonify({"error": "Email requerido"}), 400

    user = Usuario.query.filter_by(email=email).first()

    if not user:
        return jsonify({"msg": "Si el email existe, se enviará un enlace"}), 200

    import secrets

    token = secrets.token_urlsafe(32)

    reset = ContrasenaReset(usuario_id=user.id, token=token)

    db.session.add(reset)
    db.session.commit()

    msg = Message(
        subject="Recuperación de contraseña",
        sender=os.getenv("MAIL_USERNAME"),
        recipients=[user.email],
    )

    msg.body = f"""
Hola,

Haz clic en el siguiente enlace para cambiar tu contraseña:

http://127.0.0.1:5000/reset/{token}
"""

    try:
        with current_app.app_context():
            mail.send(msg)
        print("Correo enviado correctamente")
    except Exception as e:
        print("ERROR al enviar correo:", e)
        return jsonify({"error": "Error enviando correo"}), 500

    return jsonify({"msg": "Correo enviado correctamente"}), 200


# Ver el reseteo de contraseña
@auth_bp.route("/reset/<token>", methods=["GET"])
def reset_page(token):
    return render_template("reset.html", token=token)


# Crear el reseteo
@auth_bp.route("/reset/<token>", methods=["POST"])
def reset_password(token):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    new_password = data.get("password")

    if not new_password:
        return jsonify({"error": "Password requerida"}), 400

    reset = ContrasenaReset.query.filter_by(token=token).first()

    if not reset:
        return jsonify({"error": "Token inválido"}), 400

    user = Usuario.query.get(reset.usuario_id)

    import bcrypt

    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())

    user.password_hash = hashed.decode()

    db.session.delete(reset)
    db.session.commit()

    return jsonify({"msg": "Contraseña actualizada correctamente"})


# Ver login
@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


# Login Usuario
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Faltan campos"}), 400

    user = Usuario.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Credenciales inválidas"}), 401

    import bcrypt

    if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        return jsonify({"error": "Credenciales inválidas"}), 401

    session["user_id"] = user.id

    return jsonify(
        {
            "msg": "Login correcto",
            "user": {"id": user.id, "nombre": user.nombre, "email": user.email},
        }
    )

@auth_bp.route("/salir")
def salir():
    session.pop("user_id", None)
    return redirect(url_for("productos.home"))
