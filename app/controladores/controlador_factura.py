from flask import Blueprint, render_template, current_app, session, redirect, url_for, flash, request
from app.utils.auth_utils import requiere_rol

bp_factura = Blueprint("factura", __name__, template_folder="../templates")

@bp_factura.route("/historial")
@requiere_rol("cliente")
def historial_facturas():
    servicio_factura = current_app.config['servicio_factura']
    cliente_id = session.get("usuario_id")  # 👈 usamos siempre usuario_id
    facturas = servicio_factura.listar_facturas_cliente(cliente_id)
    return render_template("historial_facturas.html", facturas=facturas)

@bp_factura.route("/confirmar", methods=["GET", "POST"])
@requiere_rol("cliente")
def confirmar_compra():
    servicio_factura = current_app.config['servicio_factura']
    servicio_carrito = current_app.config['servicio_carrito']
    servicio_producto = current_app.config['servicio_producto']

    carrito = servicio_carrito.obtener_carrito()
    cliente_id = session.get("usuario_id")  # 👈 consistencia con historial

    if not carrito:
        flash("El carrito está vacío", "warning")
        return redirect(url_for("carrito.ver_carrito"))

    # 👇 corregido: usar request.method en lugar de session.get("metodo")
    if request.method == "POST":
        try:
            factura = servicio_factura.crear_factura(cliente_id, carrito)
            servicio_carrito.vaciar()
            flash(f"Compra realizada. Factura #{factura.id}", "success")
            return redirect(url_for("factura.historial_facturas"))
        except Exception as e:
            flash(str(e), "danger")
            return redirect(url_for("carrito.ver_carrito"))

    # Mostrar resumen antes de confirmar
    resumen = []
    total = 0
    for pid, cantidad in carrito.items():
        producto = servicio_producto.obtener(pid)
        subtotal = producto.precio * cantidad
        resumen.append({"producto": producto, "cantidad": cantidad, "subtotal": subtotal})
        total += subtotal

    return render_template("confirmar_compra.html", resumen=resumen, total=total)

# ✅ Nueva ruta: detalle de factura
@bp_factura.route("/detalle/<int:factura_id>")
@requiere_rol("cliente")
def detalle_factura(factura_id):
    servicio_factura = current_app.config['servicio_factura']
    factura = servicio_factura.obtener_factura(factura_id)
    return render_template("factura_detalle.html", factura=factura)
