from typing import Callable, List

class ObservadorInventario:
    def __init__(self):
        self._listeners: List[Callable[[str,int], None]] = []

    def suscribir(self, fn: Callable[[str,int], None]) -> None:
        self._listeners.append(fn)

    def notificar_stock_bajo(self, producto_id: str, stock: int) -> None:
        for fn in self._listeners:
            try:
                fn(producto_id, stock)
            except Exception as e:
                print("Error en observador:", e)
