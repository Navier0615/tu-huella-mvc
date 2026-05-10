# app/modelos/producto.py
from app import db

class Producto(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.String(50), primary_key=True)   # antes era str en dataclass
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    talla = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    imagen = db.Column(db.String(255), nullable=True)
    genero = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"<Producto {self.nombre} (${self.precio})>"

