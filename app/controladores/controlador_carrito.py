# app/controladores/controlador_carrito.py

from flask import Blueprint, render_template, current_app, request, redirect, url_for, flash
from app.utils.auth_utils import requiere_rol   # Importamos el decorador

bp_carrito = Blueprint("carrito", __name__, template_folder="../templates")

@bp_carrito.route("/")
@requiere_rol("cliente")   # Solo clientes pueden ver su carrito
def ver_carrito():
    servicio_carrito = current_app.config['servicio_carrito']
    servicio_producto = current_app.config['servicio_producto']

    carrito = servicio_carrito.obtener_carrito()
    items = []
    for pid, qty in carrito.items():
        try:
            prod = servicio_producto.obtener(pid)
            items.append({"producto": prod, "cantidad": qty})
        except Exception:
            # Si el producto ya no existe en la BD, lo ignoramos
            continue

    return render_template("carrito.html", items=items)

@bp_carrito.route("/agregar", methods=["POST"])
@requiere_rol("cliente")   # Solo clientes pueden agregar productos
def agregar_al_carrito():
    id_producto = request.form.get("id")
    cantidad = int(request.form.get("cantidad", "1"))
    servicio_carrito = current_app.config['servicio_carrito']

    try:
        servicio_carrito.agregar(id_producto, cantidad)   # 👈 ya no pasamos carrito
        flash("Producto agregado al carrito", "success")
    except Exception as e:
        flash(str(e), "danger")

    return redirect(url_for("producto.lista_productos"))

@bp_carrito.route("/quitar", methods=["POST"])
@requiere_rol("cliente")   # Solo clientes pueden quitar productos
def quitar_del_carrito():
    id_producto = request.form.get("id")
    cantidad = int(request.form.get("cantidad", "1"))
    servicio_carrito = current_app.config['servicio_carrito']

    try:
        servicio_carrito.quitar(id_producto, cantidad)   # 👈 ya no pasamos carrito
    except Exception as e:
        flash(str(e), "danger")

    return redirect(url_for("carrito.ver_carrito"))

@bp_carrito.route("/vaciar", methods=["POST"])
@requiere_rol("cliente")   # Solo clientes pueden vaciar el carrito
def vaciar_carrito():
    servicio_carrito = current_app.config['servicio_carrito']
    servicio_carrito.vaciar()
    flash("Carrito vaciado", "info")
    return redirect(url_for("carrito.ver_carrito"))

