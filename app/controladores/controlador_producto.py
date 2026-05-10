# app/controladores/controlador_producto.py

from flask import Blueprint, render_template, current_app, abort
from app.utils.auth_utils import requiere_rol   # Importamos el decorador

bp_producto = Blueprint("producto", __name__)

@bp_producto.route("/")
def lista_productos():
    servicio = current_app.config['servicio_producto']
    productos = servicio.listar_todos()
    return render_template("lista_productos.html", productos=productos)

@bp_producto.route("/producto/<id>")
def detalle_producto(id):
    servicio = current_app.config['servicio_producto']
    try:
        producto = servicio.obtener(id)
    except ValueError:
        abort(404)
    return render_template("producto.html", producto=producto)

# Rutas admin protegidas
@bp_producto.route("/admin/inventario")
@requiere_rol("administrador")   # Solo administradores
def panel_admin_inventario():
    servicio = current_app.config['servicio_producto']
    productos = servicio.listar_todos()
    return render_template("panel_admin_inventario.html", productos=productos)

@bp_producto.route("/admin/contabilidad")
@requiere_rol("administrador")   # Solo administradores
def panel_admin_contabilidad():
    # demo: datos estáticos para contabilidad
    resumen = {"ingresos": 15789.50, "egresos": 6325.20, "balance": 9464.30}
    transacciones = [
        {"id": "TXN001", "tipo": "Ingreso", "fecha": "2025-05-04 18:30", "descripcion": "Venta Zapatilla Nike Hombre", "monto": 89.99},
        {"id": "TXN002", "tipo": "Egreso", "fecha": "2025-05-04 10:15", "descripcion": "Compra Stock - Adidas", "monto": -350.00},
        {"id": "TXN003", "tipo": "Ingreso", "fecha": "2025-05-03 20:00", "descripcion": "Venta Zapatilla Puma Mujer", "monto": 89.99},
    ]
    return render_template("panel_admin_contabilidad.html", resumen=resumen, transacciones=transacciones)


