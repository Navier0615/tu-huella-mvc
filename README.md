Manual de Instalación: Tu Huella MVC

Este manual proporciona las instrucciones necesarias para configurar, instalar y ejecutar la aplicación Tu Huella MVC en un entorno local (Windows).

1. Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

Python 3.x

PostgreSQL (y una base de datos creada para el proyecto)

Git

2. Clonar el Repositorio

Abre una terminal y ejecuta los siguientes comandos para obtener el código y entrar en la carpeta del proyecto:

git clone https://github.com/Navier0615/tu-huella-mvc.git
cd tu-huella-mvc


3. Configuración del Entorno Virtual

Es fundamental usar un entorno virtual para no interferir con otras instalaciones de Python:

# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual (Windows)
.\venv\Scripts\activate


4. Instalación de Dependencias

Una vez activado el entorno virtual, instala las librerías necesarias:

Instalación automática:

pip install -r requirements.txt


Instalación manual (en caso de errores o librerías faltantes):

Si el comando anterior falla o faltan paquetes específicos, ejecuta:

pip install flask psycopg2-binary alembic werkzeug sqlalchemy flask-session flask-sqlalchemy python-dotenv requests


5. Configuración de la Base de Datos

Debes configurar la conexión a tu base de datos local de PostgreSQL.

Abre los archivos config.py y app/__init__.py.

Localiza la cadena de conexión (URL de la base de datos).

Actualiza la contraseña de PostgreSQL y el nombre de la base de datos según tu configuración local.

6. Inicialización de Tablas (Forzado)

Si al ejecutar la aplicación notas que las tablas no se han creado en tu base de datos, ejecuta el siguiente comando para forzar la creación del esquema:

python -c "from run import app; from app import db; app.app_context().push(); db.create_all(); print('¡Tablas creadas con éxito!')"


7. Ejecución de la Aplicación

Para iniciar el servidor de desarrollo, simplemente ejecuta:

python run.py


La aplicación debería estar corriendo en http://127.0.0.1:5000 o en el puerto indicado en la terminal.

Nota: Recuerda mantener siempre activo el entorno virtual (venv) mientras estés trabajando en el proyecto.