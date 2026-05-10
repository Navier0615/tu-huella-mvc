import requests
import uuid

class ServicioPagoPayPal:
    def __init__(self, client_id, client_secret, api_base):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_base = api_base
        self.token = None

    def obtener_token(self, force_refresh=False):
        """
        Obtiene y cachea el token de acceso de PayPal.
        Se puede forzar la renovación con force_refresh=True.
        """
        if self.token and not force_refresh:
            return self.token

        url = f"{self.api_base}/v1/oauth2/token"
        response = requests.post(
            url,
            data={"grant_type": "client_credentials"},
            auth=(self.client_id, self.client_secret)
        )
        response.raise_for_status()
        self.token = response.json()["access_token"]
        return self.token

    def crear_orden(self, total, return_url, cancel_url):
        """
        Crea una orden en PayPal lista para ser aprobada por el cliente.
        """
        token = self.obtener_token()
        url = f"{self.api_base}/v2/checkout/orders"
        total_str = f"{float(total):.2f}"

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": total_str
                    }
                }
            ],
            "application_context": {
                "return_url": return_url,
                "cancel_url": cancel_url,
                "brand_name": "Tu Huella MVC",
                "landing_page": "LOGIN",
                "user_action": "PAY_NOW"
            }
        }

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=payload
        )

        if response.status_code >= 400:
            print("❌ Error al crear orden:", response.text)
        response.raise_for_status()
        return response.json()

    def capturar_orden(self, order_id):
        """
        Captura una orden aprobada en PayPal.
        Maneja errores 422 (orden ya capturada o inválida).
        """
        token = self.obtener_token()
        url = f"{self.api_base}/v2/checkout/orders/{order_id}/capture"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            # Idempotencia: evita duplicados si el usuario refresca
            "PayPal-Request-Id": str(uuid.uuid4())
        }

        response = requests.post(url, headers=headers)

        if response.status_code == 422:
            # Orden ya capturada o inválida
            print("⚠️ Error 422 al capturar orden:", response.json())
            return {
                "status": "ERROR",
                "error": response.json(),
                "order_id": order_id
            }

        if response.status_code >= 400:
            print("❌ Error al capturar orden:", response.text)
        response.raise_for_status()
        return response.json()

    def obtener_orden(self, order_id):
        """
        Obtiene los detalles de una orden en PayPal.
        Útil cuando la respuesta de captura no trae purchase_units.
        """
        token = self.obtener_token()
        url = f"{self.api_base}/v2/checkout/orders/{order_id}"

        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        if response.status_code >= 400:
            print("❌ Error al obtener orden:", response.text)
        response.raise_for_status()
        return response.json()

    def reembolsar_pago(self, capture_id):
        """
        Procesa un reembolso en PayPal a partir de un capture_id.
        """
        token = self.obtener_token()
        url = f"{self.api_base}/v2/payments/captures/{capture_id}/refund"

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        if response.status_code == 201:
            print("✅ Reembolso exitoso:", response.json())
            return {"ok": True, "data": response.json()}
        else:
            print("❌ Error al reembolsar:", response.status_code, response.text)
            return {
                "ok": False,
                "status": response.status_code,
                "error": response.json()
            }
