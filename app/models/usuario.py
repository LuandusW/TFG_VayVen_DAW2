from app import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    rol = db.Column(db.String(20), default="usuario")
    activo = db.Column(db.Boolean, default=True)
    creacion = db.Column(db.DateTime, default=datetime.utcnow)
    
    productos = db.relationship("Producto", backref="vendedor", lazy=True)