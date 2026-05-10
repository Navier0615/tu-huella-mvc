# app/modelos/usuario.py
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)  # opcional
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False, default="cliente")

    # Relación con facturas
    facturas = db.relationship("Factura", back_populates="cliente", lazy=True)

    def __init__(self, username, password, rol="cliente", email=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.rol = rol

    def set_password(self, password):
        """Guarda la contraseña hasheada"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica la contraseña"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Usuario {self.username} ({self.rol})>"
