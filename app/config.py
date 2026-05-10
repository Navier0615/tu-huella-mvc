import os

class Configuracion:
    SECRET_KEY = "clave_secreta"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:miPassword123@localhost:5432/tu_huella_mvc"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de sesiones en BD
    SESSION_TYPE = "sqlalchemy"

    # PayPal Sandbox
    PAYPAL_CLIENT_ID = "AaZqDHmCFpF7qlOMYtiP8n9RwXf-laqhawhULky4695xzyNLV8ql8OrF70ETyZS8QaQ8E_7TS1EdiRXd"
    PAYPAL_CLIENT_SECRET = "EAhghsf5bWn7KASQu3_p0_e85eSFvyOMYhffxp0G7oXWu3bbs8Fyphc1irG_4fJ81xCnr3EshEImr-yD"
    PAYPAL_API_BASE = "https://api-m.sandbox.paypal.com"





    
