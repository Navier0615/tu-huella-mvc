from app import db

class CarritoProducto(db.Model):
    __tablename__ = "carrito_producto"

    carrito_id = db.Column(db.Integer, db.ForeignKey("carritos.id"), primary_key=True)
    producto_id = db.Column(db.String(50), db.ForeignKey("productos.id"), primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)

    carrito = db.relationship("Carrito", back_populates="productos")
    producto = db.relationship("Producto")
