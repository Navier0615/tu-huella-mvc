from typing import Optional
from ..modelos.usuario import Usuario

class RepositorioMemoriaUsuario:
    def __init__(self):
        self._usuarios = {}  # username -> Usuario

    def crear_usuario(self, username: str, password: str, rol: str) -> None:
        self._usuarios[username] = Usuario(username, password, rol)

    def obtener_por_username(self, username: str) -> Optional[Usuario]:
        return self._usuarios.get(username)
