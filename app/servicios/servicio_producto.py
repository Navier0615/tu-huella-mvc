# app/servicios/servicio_producto.py
from typing import List
from app.modelos.producto import Producto
from app import db
from ..observadores.observador_inventario import ObservadorInventario

class ServicioProducto:
    def __init__(self, db, observador: ObservadorInventario, umbral_bajo: int = 5):
        self.db = db
        self.observador = observador
        self.umbral_bajo = umbral_bajo

    def listar_todos(self) -> List[Producto]:
        """Devuelve todos los productos de la BD"""
        return Producto.query.all()

    def obtener(self, id: str) -> Producto:
        """Obtiene un producto por ID o lanza ValueError si no existe"""
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError("Producto no existe")
        return producto

    def crear(self, producto: Producto) -> None:
        """Crea un nuevo producto en la BD"""
        if producto.precio <= 0:
            raise ValueError("Precio inválido")
        if producto.talla <= 0:
            raise ValueError("Talla inválida")

        self.db.session.add(producto)
        self.db.session.commit()

        if producto.stock < self.umbral_bajo:
            self.observador.notificar_stock_bajo(producto.id, producto.stock)

    def actualizar_stock(self, id: str, nuevo_stock: int) -> None:
        """Actualiza el stock de un producto"""
        producto = Producto.query.get(id)
        if not producto:
            raise ValueError("Producto no existe")

        producto.stock = nuevo_stock
        self.db.session.commit()

        if nuevo_stock < self.umbral_bajo:
            self.observador.notificar_stock_bajo(id, nuevo_stock)
