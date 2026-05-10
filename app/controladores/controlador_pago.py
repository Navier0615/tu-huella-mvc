from flask import Blueprint, current_app, redirect, request, url_for, render_template, flash, session

bp_pago = Blueprint("pago", __name__)

@bp_pago.route("/paypal/crear")
def crear_pago():
    servicio_pago = current_app.config["servicio_pago"]
    servicio_carrito = current_app.config["servicio_carrito"]

    total = servicio_carrito.calcular_total()

    if total <= 0:
        return "El carrito está vacío o el total es inválido", 400

    return_url = url_for("pago.retorno_pago", _external=True)
    cancel_url = url_for("pago.cancelar_pago", _external=True)

    orden = servicio_pago.crear_orden(total, return_url, cancel_url)

    for link in orden["links"]:
        if link["rel"] == "approve":
            return redirect(link["href"])

    return "No se pudo generar el link de aprobación", 400


@bp_pago.route("/paypal/retorno")
def retorno_pago():
    servicio_pago = current_app.config["servicio_pago"]
    servicio_factura = current_app.config["servicio_factura"]
    servicio_auditoria = current_app.config["servicio_auditoria"]
    servicio_carrito = current_app.config["servicio_carrito"]

    order_id = request.args.get("token")

    try:
        # ✅ Capturar la orden en PayPal
        captura = servicio_pago.capturar_orden(order_id)
        print("DEBUG captura:", captura)

        # ⚠️ Fallback: si no trae purchase_units, pedir detalles de la orden
        if "purchase_units" not in captura:
            captura = servicio_pago.obtener_orden(order_id)
            print("DEBUG obtener_orden:", captura)

        if captura.get("status") == "COMPLETED":
            items = servicio_carrito.obtener_items()

            # ✅ Extraer capture_id del pago de forma robusta
            capture_id = None
            try:
                if "purchase_units" in captura and "payments" in captura["purchase_units"][0]:
                    capture_id = captura["purchase_units"][0]["payments"]["captures"][0]["id"]
                elif "id" in captura:
                    # fallback: usar id de la orden como referencia
                    capture_id = captura["id"]
            except Exception as e:
                print("⚠️ No se pudo extraer capture_id:", str(e))

            # ✅ Obtener cliente desde sesión
            cliente_id = session.get("usuario_id")
            if not cliente_id:
                flash("No hay cliente en sesión", "danger")
                return redirect(url_for("carrito.ver_carrito"))

            # ⚠️ Evitar facturas duplicadas si el usuario refresca
            facturas_existentes = servicio_factura.listar_facturas_cliente(cliente_id)
            if any(f.capture_id == capture_id for f in facturas_existentes if capture_id):
                flash("Esta orden ya fue procesada", "info")
                return redirect(url_for("factura.historial_facturas"))

            # ✅ Crear factura con cliente, items y capture_id
            factura = servicio_factura.crear_factura_desde_items(
                cliente_id,
                items,
                capture_id=capture_id
            )

            servicio_auditoria.registrar_evento("Pago", f"Factura {factura.id} creada desde PayPal")

            servicio_carrito.vaciar()

            return render_template("pago_exitoso.html", factura=factura, captura=captura)
        else:
            return render_template("pago_fallido.html", estado=captura.get("status"))

    except Exception as e:
        print("⚠️ Error en retorno_pago:", str(e))
        return render_template("pago_fallido.html", estado="ERROR")


@bp_pago.route("/paypal/cancelar")
def cancelar_pago():
    return render_template("pago_cancelado.html")


# ✅ Ruta para procesar reembolso
@bp_pago.route("/reembolso/<capture_id>", methods=["POST"])
def reembolso(capture_id):
    servicio_pago = current_app.config["servicio_pago"]
    resultado = servicio_pago.reembolsar_pago(capture_id)

    if resultado["ok"]:
        flash("Reembolso exitoso", "success")
    else:
        error_msg = resultado.get("error", {}).get("message", "Error desconocido")
        flash(f"Error al reembolsar: {error_msg}", "danger")

    return redirect(url_for("bp_administracion.panel"))
