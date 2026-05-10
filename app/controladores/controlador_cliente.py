from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
from app.utils.auth_utils import requiere_rol

bp_cliente = Blueprint("cliente", __name__, template_folder="../templates")

@bp_cliente.route("/perfil", methods=["GET", "POST"])
@requiere_rol("cliente")
def perfil_cliente():
    servicio_cliente = current_app.config['servicio_cliente']
    cliente_id = session.get("usuario_id")

    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        telefono = request.form.get("telefono")
        direccion = request.form.get("direccion")

        try:
            servicio_cliente.actualizar_datos(cliente_id, nombre, correo, telefono, direccion)
            flash("Perfil actualizado correctamente", "success")
        except Exception as e:
            flash(str(e), "danger")

        return redirect(url_for("cliente.perfil_cliente"))

    cliente = servicio_cliente.obtener_por_id(cliente_id)
    return render_template("perfil_cliente.html", cliente=cliente)
