from datetime import datetime
from app.modelos.factura import Factura
from app.modelos.detalle_factura import DetalleFactura
from app.modelos.producto import Producto

class ServicioFactura:
    def __init__(self, db):
        self.db = db

    def crear_factura(self, cliente_id: int, carrito: dict) -> Factura:
        """
        Genera una factura con sus detalles a partir de un carrito en forma de dict {producto_id: cantidad}.
        """
        if not carrito:
            raise ValueError("El carrito está vacío")

        total = 0.0
        factura = Factura(cliente_id=cliente_id, total=0.0, fecha=datetime.utcnow())
        self.db.session.add(factura)
        self.db.session.flush()  # ✅ asegura que factura.id exista

        for producto_id, cantidad in carrito.items():
            producto = Producto.query.get(producto_id)
            if not producto:
                continue

            subtotal = producto.precio * cantidad
            detalle = DetalleFactura(
                factura_id=factura.id,
                producto_id=producto.id,
                cantidad=cantidad,
                subtotal=subtotal
            )
            total += subtotal
            self.db.session.add(detalle)

            # Reducir stock del producto
            producto.stock -= cantidad

        factura.total = total
        self.db.session.commit()
        return factura

    def crear_factura_desde_items(self, cliente_id: int, items_carrito: list, capture_id: str = None) -> Factura:
        """
        Genera una factura a partir de la lista de items que devuelve servicio_carrito.obtener_items().
        Cada item es un dict con {producto, cantidad, subtotal}.
        Guarda el capture_id de PayPal si se proporciona.
        """
        if not items_carrito:
            raise ValueError("El carrito está vacío")

        total = 0.0
        factura = Factura(
            cliente_id=cliente_id,
            total=0.0,
            fecha=datetime.utcnow(),
            capture_id=capture_id   # ✅ se guarda el capture_id
        )
        self.db.session.add(factura)
        self.db.session.flush()  # ✅ asegura que factura.id exista

        for item in items_carrito:
            producto = item["producto"]
            cantidad = item["cantidad"]
            subtotal = item["subtotal"]

            detalle = DetalleFactura(
                factura_id=factura.id,
                producto_id=producto.id,
                cantidad=cantidad,
                subtotal=subtotal
            )
            total += subtotal
            self.db.session.add(detalle)

            # Reducir stock
            producto.stock -= cantidad

        factura.total = total
        self.db.session.commit()
        return factura

    def crear_factura_desde_pago(self, cliente_id: int, captura: dict) -> Factura:
        """
        Genera una factura a partir de la respuesta de PayPal (captura de orden).
        Guarda el ID de transacción de PayPal en la factura.
        """
        if captura.get("status") != "COMPLETED":
            raise ValueError("El pago no fue completado")

        total = float(captura["purchase_units"][0]["payments"]["captures"][0]["amount"]["value"])
        transaccion_id = captura["purchase_units"][0]["payments"]["captures"][0]["id"]

        factura = Factura(
            cliente_id=cliente_id,
            total=total,
            fecha=datetime.utcnow(),
            capture_id=transaccion_id
        )
        self.db.session.add(factura)
        self.db.session.commit()
        return factura

    def listar_facturas_cliente(self, cliente_id: int):
        """Devuelve todas las facturas de un cliente"""
        return Factura.query.filter_by(cliente_id=cliente_id).order_by(Factura.fecha.desc()).all()

    def obtener_factura(self, factura_id: int) -> Factura:
        """Devuelve una factura por ID"""
        return Factura.query.get_or_404(factura_id)
    
    def listar_facturas(self):
        """Devuelve absolutamente todas las facturas de la tienda (para reportes)"""
        return Factura.query.order_by(Factura.fecha.desc()).all()
