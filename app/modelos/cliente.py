from app import db

class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(200), nullable=True)

    # Relaciones futuras: carritos, facturas, etc.
    # carritos = db.relationship("Carrito", backref="cliente", lazy=True)
    # facturas = db.relationship("Factura", backref="cliente", lazy=True)

    def __repr__(self):
        return f"<Cliente {self.nombre}>"
