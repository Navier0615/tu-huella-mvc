from typing import List, Optional
from .repositorio_base import RepositorioProducto
from ..modelos.producto import Producto

class RepositorioMemoriaProducto(RepositorioProducto):
    def __init__(self, inicial: List[Producto] = None):
        self._almacen = {}
        if inicial:
            for p in inicial:
                self._almacen[p.id] = p

    def listar(self) -> List[Producto]:
        return list(self._almacen.values())

    def obtener_por_id(self, id: str) -> Optional[Producto]:
        return self._almacen.get(id)

    def guardar(self, producto: Producto) -> None:
        self._almacen[producto.id] = producto

    def actualizar_stock(self, id: str, nuevo_stock: int) -> None:
        p = self._almacen.get(id)
        if not p:
            raise ValueError("Producto no encontrado")
        p.stock = nuevo_stock
        self._almacen[id] = p
