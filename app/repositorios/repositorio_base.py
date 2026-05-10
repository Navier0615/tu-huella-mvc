from abc import ABC, abstractmethod
from typing import List, Optional
from ..modelos.producto import Producto

class RepositorioProducto(ABC):
    @abstractmethod
    def listar(self) -> List[Producto]:
        pass

    @abstractmethod
    def obtener_por_id(self, id: str) -> Optional[Producto]:
        pass

    @abstractmethod
    def guardar(self, producto: Producto) -> None:
        pass

    @abstractmethod
    def actualizar_stock(self, id: str, nuevo_stock: int) -> None:
        pass
