from flask import session, redirect, url_for, flash
from typing import Callable
from ..repositorios.repositorio_usuario import RepositorioMemoriaUsuario

class ServicioAutenticacion:
    def __init__(self, repo: RepositorioMemoriaUsuario):
        self.repo = repo

    def login(self, username: str, password: str) -> bool:
        user = self.repo.obtener_por_username(username)
        if not user:
            return False
        if user.password != password:
            return False
        # guardamos en session
        session['usuario'] = {'username': user.username, 'rol': user.rol}
        return True

    def logout(self):
        if 'usuario' in session:
            session.pop('usuario')

    def usuario_actual(self):
        return session.get('usuario')

    # decorador para proteger rutas por rol
    def requiere_rol(self, rol_requerido: str):
        def wrapper(func: Callable):
            def inner(*args, **kwargs):
                usuario = session.get('usuario')
                if not usuario:
                    flash("Debes iniciar sesión", "warning")
                    return redirect(url_for('auth.login'))
                if usuario.get('rol') != rol_requerido:
                    flash("No tienes permisos para acceder a esta página", "danger")
                    return redirect(url_for('producto.lista_productos'))
                return func(*args, **kwargs)
            inner.__name__ = func.__name__
            return inner
        return wrapper

    # decorador para permitir varios roles
    def requiere_roles(self, roles: list):
        def wrapper(func: Callable):
            def inner(*args, **kwargs):
                usuario = session.get('usuario')
                if not usuario:
                    flash("Debes iniciar sesión", "warning")
                    return redirect(url_for('auth.login'))
                if usuario.get('rol') not in roles:
                    flash("No tienes permisos para acceder a esta página", "danger")
                    return redirect(url_for('producto.lista_productos'))
                return func(*args, **kwargs)
            inner.__name__ = func.__name__
            return inner
        return wrapper
