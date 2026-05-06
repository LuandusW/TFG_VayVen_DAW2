from app import db

class ContrasenaReset(db.Model):
    __tablename__ = "contrasena_resets"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    creacion = db.Column(db.DateTime, server_default=db.func.now())