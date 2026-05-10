# app/controladores/controlador_compra.py

from flask import Blueprint, render_template, session, current_app
from app.utils.auth_utils import requiere_rol   # Importamos el decorador

bp_compra = Blueprint("compra", __name__, template_folder="../templates")

@bp_compra.route("/pagar", methods=["GET", "POST"])
@requiere_rol("cliente")   # Solo clientes pueden pagar
def pagar():
    servicio_producto = current_app.config['servicio_producto']
    carrito = session.get("carrito", {})
    items = []
    total = 0.0

    for pid, qty in carrito.items():
        prod = servicio_producto.obtener(pid)
        items.append({"producto": prod, "cantidad": qty})
        total += prod.precio * qty

    # En demo: vaciar carrito (en real persistir factura en BD)
    session['carrito'] = {}

    return render_template(
        "confirmacion_pedido.html",
        items=items,
        total=total,
        orden_id=f"ORD-{int(__import__('time').time())}"
    )

