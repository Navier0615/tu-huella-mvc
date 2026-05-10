from app import db
from datetime import datetime

class Factura(db.Model):
    __tablename__ = "facturas"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    total = db.Column(db.Float, nullable=False, default=0.0)

    # 👇 ID de transacción PayPal (único para evitar duplicados)
    capture_id = db.Column(db.String(100), nullable=True, unique=True, index=True)

    # Relación con Usuario
    cliente_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    cliente = db.relationship("Usuario", back_populates="facturas")

    # Relación con DetalleFactura
    detalles = db.relationship(
        "DetalleFactura",
        back_populates="factura",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Factura id={self.id} cliente_id={self.cliente_id} total={self.total} capture_id={self.capture_id}>"
