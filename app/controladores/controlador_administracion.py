from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.utils.auth_utils import requiere_rol

bp_administracion = Blueprint("administracion", __name__, template_folder="../templates")

@bp_administracion.route("/productos")
@requiere_rol("administrador")
def administrar_productos():
    servicio = current_app.config['servicio_administracion']
    productos = servicio.listar_productos()
    return render_template("administracion_productos.html", productos=productos)

@bp_administracion.route("/usuarios")
@requiere_rol("administrador")
def administrar_usuarios():
    servicio = current_app.config['servicio_administracion']
    usuarios = servicio.listar_usuarios()
    return render_template("administracion_usuarios.html", usuarios=usuarios)

@bp_administracion.route("/ventas")
@requiere_rol("administrador")
def administrar_ventas():
    servicio = current_app.config['servicio_administracion']
    facturas = servicio.listar_facturas()
    return render_template("administracion_ventas.html", facturas=facturas)

@bp_administracion.route("/inventario")
@requiere_rol("administrador")
def administrar_inventario():
    servicio = current_app.config['servicio_administracion']
    productos = servicio.listar_productos()
    return render_template("administracion_inventario.html", productos=productos)

@bp_administracion.route("/contabilidad")
@requiere_rol("administrador")
def administrar_contabilidad():
    servicio = current_app.config['servicio_administracion']
    facturas = servicio.listar_facturas()
    return render_template("administracion_contabilidad.html", facturas=facturas)
