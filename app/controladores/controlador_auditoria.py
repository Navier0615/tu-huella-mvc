from flask import Blueprint, render_template, current_app
from app.utils.auth_utils import requiere_rol

bp_auditoria = Blueprint("auditoria", __name__, template_folder="../templates")

@bp_auditoria.route("/eventos")
@requiere_rol("administrador")
def ver_eventos():
    servicio = current_app.config['servicio_auditoria']
    eventos = servicio.listar_eventos()
    return render_template("auditoria_eventos.html", eventos=eventos)
