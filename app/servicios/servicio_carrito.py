from typing import Dict, List
from flask import session
from app.modelos.producto import Producto
from app import db

# El carrito se guarda en sesión como {id_producto: cantidad}
TipoCarrito = Dict[str, int]

class ServicioCarrito:
    def __init__(self, db, umbral_bajo: int = 5):
        self.db = db
        self.umbral_bajo = umbral_bajo

    def obtener_carrito(self) -> TipoCarrito:
        """Devuelve el carrito actual desde la sesión"""
        return session.get("carrito", {})

    def guardar_carrito(self, carrito: TipoCarrito):
        """Guarda el carrito en la sesión"""
        session["carrito"] = carrito

    def agregar(self, id_producto: str, cantidad: int = 1) -> TipoCarrito:
        """Agrega un producto al carrito"""
        producto = Producto.query.get(id_producto)
        if not producto:
            raise ValueError("Producto no existe")
        if producto.stock < cantidad:
            raise ValueError("Stock insuficiente")

        carrito = self.obtener_carrito()
        carrito[id_producto] = carrito.get(id_producto, 0) + cantidad
        self.guardar_carrito(carrito)

        # Actualizar stock en BD
        producto.stock -= cantidad
        self.db.session.commit()

        return carrito

    def quitar(self, id_producto: str, cantidad: int = 1) -> TipoCarrito:
        """Quita un producto del carrito"""
        carrito = self.obtener_carrito()
        actual = carrito.get(id_producto, 0)
        if actual <= 0:
            return carrito

        quitar = min(cantidad, actual)
        carrito[id_producto] = actual - quitar
        if carrito[id_producto] == 0:
            del carrito[id_producto]
        self.guardar_carrito(carrito)

        # Devolver stock a la BD
        producto = Producto.query.get(id_producto)
        if producto:
            producto.stock += quitar
            self.db.session.commit()

        return carrito

    def vaciar(self) -> None:
        """Vacía el carrito"""
        session["carrito"] = {}

    # 👇 NUEVOS MÉTODOS

    def calcular_total(self) -> float:
        """Calcula el total del carrito sumando precio * cantidad"""
        carrito = self.obtener_carrito()
        total = 0.0
        for id_producto, cantidad in carrito.items():
            producto = Producto.query.get(id_producto)
            if producto:
                total += producto.precio * cantidad
        return total

    def obtener_items(self) -> List[dict]:
        """
        Devuelve una lista de items con producto, cantidad y subtotal.
        Esto es lo que se usará en ServicioFactura.
        """
        carrito = self.obtener_carrito()
        items = []
        for id_producto, cantidad in carrito.items():
            producto = Producto.query.get(id_producto)
            if producto:
                items.append({
                    "producto": producto,
                    "cantidad": cantidad,
                    "subtotal": producto.precio * cantidad
                })
        return items
