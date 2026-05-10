from app.modelos.cliente import Cliente
from app import db

class ServicioCliente:
    def __init__(self, db):
        self.db = db

    def obtener_por_id(self, cliente_id: int) -> Cliente:
        return Cliente.query.get_or_404(cliente_id)

    def actualizar_datos(self, cliente_id: int, nombre: str, correo: str, telefono: str, direccion: str):
        cliente = Cliente.query.get_or_404(cliente_id)
        cliente.nombre = nombre
        cliente.correo = correo
        cliente.telefono = telefono
        cliente.direccion = direccion
        self.db.session.commit()
        return cliente
