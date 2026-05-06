from app import db

class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)

    vendedor_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    titulo = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Numeric(10, 2), nullable=False)

    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey("categorias.id")
    )

    categoria = db.relationship("Categoria")

    foto_url = db.Column(db.String(500))
    creacion = db.Column(db.DateTime)

    