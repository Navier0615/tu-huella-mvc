from app import db

class DetalleFactura(db.Model):
    __tablename__ = "detalle_factura"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    factura_id = db.Column(db.Integer, db.ForeignKey("facturas.id"), nullable=False)
    producto_id = db.Column(db.String(50), db.ForeignKey("productos.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    factura = db.relationship("Factura", back_populates="detalles")
    producto = db.relationship("Producto")

