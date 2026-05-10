from app.modelos.producto import Producto
from app.modelos.usuario import Usuario
from app.modelos.factura import Factura
from app import db

class ServicioAdministracion:
    def __init__(self, db):
        self.db = db

    # --- Productos ---
    def listar_productos(self):
        return Producto.query.all()

    def crear_producto(self, id, nombre, precio, talla, stock, imagen, genero):
        nuevo = Producto(id=id, nombre=nombre, precio=precio, talla=talla, stock=stock, imagen=imagen, genero=genero)
        self.db.session.add(nuevo)
        self.db.session.commit()
        return nuevo

    def actualizar_producto(self, producto_id, **kwargs):
        producto = Producto.query.get_or_404(producto_id)
        for key, value in kwargs.items():
            setattr(producto, key, value)
        self.db.session.commit()
        return producto

    def eliminar_producto(self, producto_id):
        producto = Producto.query.get_or_404(producto_id)
        self.db.session.delete(producto)
        self.db.session.commit()

    # --- Usuarios ---
    def listar_usuarios(self):
        return Usuario.query.all()

    # --- Facturas / Ventas ---
    def listar_facturas(self):
        return Factura.query.all()
