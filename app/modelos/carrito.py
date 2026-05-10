from app import db

class Carrito(db.Model):
    __tablename__ = "carritos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    # Relación con productos (N:M)
    productos = db.relationship(
        "CarritoProducto",
        back_populates="carrito",
        cascade="all, delete-orphan"
    )

    def calcular_total(self):
        """Suma el total del carrito multiplicando precio * cantidad de cada producto"""
        return sum(item.producto.precio * item.cantidad for item in self.productos)
