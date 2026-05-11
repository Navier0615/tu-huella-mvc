from app import create_app  # <--- Cambiado de 'crear_aplicacion' a 'create_app'

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
