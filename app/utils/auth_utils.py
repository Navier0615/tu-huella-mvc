# app/utils/auth_utils.py
from functools import wraps
from flask import session, redirect, url_for, flash

def requiere_rol(roles):
    """
    Decorador para restringir acceso según rol.
    Puede recibir un string (un rol) o una lista de roles.
    """
    if isinstance(roles, str):
        roles = [roles]

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'rol' not in session:
                flash("Debes iniciar sesión.", "warning")
                return redirect(url_for("auth.login"))
            if session['rol'] not in roles:
                flash("No tienes permisos para acceder a esta página.", "danger")
                return redirect(url_for("producto.lista_productos"))
            return f(*args, **kwargs)
        return wrapper
    return decorator
