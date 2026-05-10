from flask import Blueprint, render_template, current_app
from app.utils.auth_utils import requiere_rol

bp_reportes = Blueprint("reportes", __name__, template_folder="../templates")

@bp_reportes.route("/ventas")
@requiere_rol("administrador")
def reporte_ventas():
    servicio_factura = current_app.config['servicio_factura']
    facturas = servicio_factura.listar_facturas()
    total = sum(f.total for f in facturas)
    return render_template("reporte_ventas.html", facturas=facturas, total=total)
