from app.modelos.auditoria import Auditoria
from app import db

class ServicioAuditoria:
    def __init__(self, db):
        self.db = db

    def registrar_evento(self, usuario, accion, entidad, entidad_id=None):
        evento = Auditoria(usuario=usuario, accion=accion, entidad=entidad, entidad_id=entidad_id)
        self.db.session.add(evento)
        self.db.session.commit()

    def listar_eventos(self, limite=50):
        return Auditoria.query.order_by(Auditoria.fecha.desc()).limit(limite).all()
