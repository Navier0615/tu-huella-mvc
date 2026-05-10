# app/controladores/controlador_autenticacion.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

# Blueprint para el módulo de autenticación
bp_auth = Blueprint('auth', __name__, template_folder='../vistas')

# Página de inicio de sesión
@bp_auth.route("/login", methods=["GET", "POST"])
def login():
    from app.modelos.usuario import Usuario
    if request.method == "POST":
        email_or_user = request.form.get("email")  # puede ser email o username
        password = request.form.get("password")

        usuario = Usuario.query.filter(
            (Usuario.email == email_or_user) | (Usuario.username == email_or_user)
        ).first()

        if usuario and usuario.check_password(password):
            session["usuario"] = usuario.username
            session["rol"] = usuario.rol
            session["cliente_id"] = usuario.id
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("producto.lista_productos"))

        flash("Usuario o contraseña incorrecta", "danger")

    return render_template("login.html")

# Cierre de sesión
@bp_auth.route('/logout')
def logout():
    # Limpiamos toda la sesión (usuario, rol, cliente_id)
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth.login'))


@bp_auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Crear nuevo usuario
        nuevo = Usuario(username=username, email=email, password=password, rol="cliente")
        db.session.add(nuevo)
        db.session.commit()

        flash("Usuario registrado con éxito. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for('auth.login'))

    return render_template('registro.html')


