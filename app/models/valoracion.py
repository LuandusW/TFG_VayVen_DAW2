from app import db

class Valoracion(db.Model):
    __tablename__ = "valoraciones"

    id = db.Column(db.Integer, primary_key=True)

    autor_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    destinatario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    puntuacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.Text)
    creacion = db.Column(db.DateTime)

    autor = db.relationship("Usuario", foreign_keys=[autor_id])
    destinatario = db.relationship("Usuario", foreign_keys=[destinatario_id])