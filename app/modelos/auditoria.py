from app import db
from datetime import datetime

class Auditoria(db.Model):
    __tablename__ = "auditoria"

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(50), nullable=False)
    accion = db.Column(db.String(100), nullable=False)
    entidad = db.Column(db.String(50), nullable=False)   # Ej: Producto, Usuario, Factura
    entidad_id = db.Column(db.String(50), nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
