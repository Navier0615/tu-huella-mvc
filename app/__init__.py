from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Configuracion
from sqlalchemy.exc import ProgrammingError, OperationalError

# Inicializamos SQLAlchemy y Migrate
db = SQLAlchemy()
migrate = Migrate()
session = Session()

def create_app():  # 👈 renombrado para que Flask lo detecte
    app = Flask(__name__, template_folder="vistas", static_folder="static")
    app.config.from_object(Configuracion)

    # 🔑 Clave secreta para firmar cookies de sesión
    app.secret_key = "9f2c4a8e7b1d4e6f9a3c2b7d8f1e0c4d9a7b6c5d4e3f2a1b0c9d8e7f6a5b4c3"

    # Configuración de conexión a PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "postgresql+psycopg2://postgres:admin123@localhost:5432/tu_huella_db"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ✅ Configuración para sesiones en la base de datos
    app.config["SESSION_TYPE"] = "sqlalchemy"
    app.config["SESSION_SQLALCHEMY"] = db

    db.init_app(app)
    migrate.init_app(app, db)  # 👈 habilita flask db

    # Inicializamos Flask-Session después de configurar
    session.init_app(app)

    # Importar modelos DESPUÉS de inicializar db
    with app.app_context():
        from .modelos.producto import Producto
        from .modelos.usuario import Usuario
        from .modelos.cliente import Cliente
        from .modelos.carrito import Carrito
        from .modelos.carrito_producto import CarritoProducto
        from .modelos.factura import Factura
        from .modelos.detalle_factura import DetalleFactura
        from .modelos.auditoria import Auditoria

        try:
            # Semillas de productos
            if Producto.query.count() == 0:
                semillas = [
                    Producto(id="p1", nombre="Zapatilla Runner", precio=120.0, talla=42, stock=25, imagen="/static/images/runner.jpg", genero="HOMBRE"),
                    Producto(id="p2", nombre="Zapatilla Lifestyle", precio=150.0, talla=39, stock=18, imagen="/static/images/lifestyle.jpg", genero="MUJER"),
                    Producto(id="p3", nombre="Zapatilla Trail", precio=180.0, talla=44, stock=12, imagen="/static/images/trail.jpg", genero="HOMBRE"),
                    Producto(id="p4", nombre="Zapatilla Casual", precio=90.0, talla=41, stock=30, imagen="/static/images/casual.jpg", genero="UNISEX"),
                    Producto(id="p5", nombre="Zapatilla Sport", precio=130.0, talla=43, stock=6, imagen="/static/images/sport.jpg", genero="HOMBRE"),
                ]
                db.session.add_all(semillas)
                db.session.commit()

            # Semillas de usuarios con email
            if Usuario.query.count() == 0:
                admin = Usuario(
                    username="admin",
                    email="admin@demo.com",
                    password="admin123",
                    rol="administrador"
                )
                cliente = Usuario(
                    username="cliente",
                    email="cliente@demo.com",
                    password="cliente123",
                    rol="cliente"
                )
                db.session.add_all([admin, cliente])
                db.session.commit()

            # Semilla de cliente
            if Cliente.query.count() == 0:
                demo = Cliente(
                    nombre="Juan Pérez",
                    correo="juan@correo.com",
                    telefono="3001234567",
                    direccion="Calle 123"
                )
                db.session.add(demo)
                db.session.commit()

        except (ProgrammingError, OperationalError):
            # Si las tablas aún no existen (durante migraciones), ignoramos
            pass

    # Observador de inventario
    from .observadores.observador_inventario import ObservadorInventario
    observador = ObservadorInventario()
    observador.suscribir(lambda pid, stock: print(f"[ALERTA] Stock bajo: {pid} -> {stock}"))

    # Servicios
    from .servicios.servicio_producto import ServicioProducto
    from .servicios.servicio_carrito import ServicioCarrito
    from .servicios.servicio_factura import ServicioFactura
    from .servicios.servicio_autenticacion import ServicioAutenticacion
    from .servicios.servicio_cliente import ServicioCliente
    from .servicios.servicio_administracion import ServicioAdministracion
    from .servicios.servicio_auditoria import ServicioAuditoria
    from .servicios.servicio_pago import ServicioPagoPayPal

    servicio_producto = ServicioProducto(db, observador)
    servicio_carrito = ServicioCarrito(db)
    servicio_factura = ServicioFactura(db)
    servicio_auth = ServicioAutenticacion(db)
    servicio_cliente = ServicioCliente(db)
    servicio_administracion = ServicioAdministracion(db)
    servicio_auditoria = ServicioAuditoria(db)
    servicio_pago = ServicioPagoPayPal(
        app.config["PAYPAL_CLIENT_ID"],
        app.config["PAYPAL_CLIENT_SECRET"],
        app.config["PAYPAL_API_BASE"]
    )

    app.config['servicio_producto'] = servicio_producto
    app.config['servicio_carrito'] = servicio_carrito
    app.config['servicio_factura'] = servicio_factura
    app.config['servicio_auth'] = servicio_auth
    app.config['servicio_cliente'] = servicio_cliente
    app.config['servicio_administracion'] = servicio_administracion
    app.config['servicio_auditoria'] = servicio_auditoria
    app.config['servicio_pago'] = servicio_pago

    # Blueprints
    from .controladores.controlador_producto import bp_producto
    from .controladores.controlador_carrito import bp_carrito
    from .controladores.controlador_factura import bp_factura
    from .controladores.controlador_compra import bp_compra
    from .controladores.controlador_autenticacion import bp_auth
    from .controladores.controlador_cliente import bp_cliente
    from .controladores.controlador_administracion import bp_administracion
    from .controladores.controlador_auditoria import bp_auditoria
    from .controladores.controlador_reportes import bp_reportes
    from .controladores.controlador_pago import bp_pago

    app.register_blueprint(bp_producto)
    app.register_blueprint(bp_carrito, url_prefix="/carrito")
    app.register_blueprint(bp_factura, url_prefix="/factura")
    app.register_blueprint(bp_compra, url_prefix="/compra")
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_cliente, url_prefix="/cliente")
    app.register_blueprint(bp_administracion, url_prefix="/administracion")
    app.register_blueprint(bp_auditoria, url_prefix="/auditoria")
    app.register_blueprint(bp_reportes, url_prefix="/reportes")
    app.register_blueprint(bp_pago, url_prefix="/pago")

    return app
