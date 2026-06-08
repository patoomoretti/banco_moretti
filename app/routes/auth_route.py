from flask import Blueprint, render_template, request, redirect, session
from utils.helpers import *
from models.usuarios import Usuario

auth_bp = Blueprint("auth", __name__)

# # # # # INICIO SESION CLIENTE
@auth_bp.route("/login", methods=["GET", "POST"])
def login_view():
    if request.method == "POST":
        dni = int(request.form.get("dni"))
        pin = int(request.form.get("pin"))
        return loguear_cuenta(dni,pin)
        
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout_view():
    session.clear()
    return render_template("auth/cerrar_sesion.html")

@auth_bp.route("/registrar", methods=["GET", "POST"])
def registrar_view():
    if request.method == "POST":
        dni = int(request.form["dni"])
        pin = int(request.form["pin"])
        return registrar_cuenta(dni,pin)
    
    return render_template("auth/registrar.html", mensaje=None)


@auth_bp.route("/restablecer", methods=["GET","POST"])
def restablecer_view():
    if request.method == "POST":
        dni = int(request.form["dni"])
        pin = int(request.form["pin"])
        pin_reingresar = int(request.form["pin_reingresar"])
        return restablecer_pin(dni,pin,pin_reingresar)
    
    return render_template("auth/restablecer.html", mensaje=None)





# # # # # INICIO SESION ADMIN
@auth_bp.route("/admin", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        dni = int(request.form.get("dni"))
        pin = int(request.form.get("pin"))
        return loguear_cuenta_admin(dni,pin)
        
    return render_template("auth/login_admin.html")


@auth_bp.route("/registrar_empleado", methods=["GET", "POST"])
def registrar_empleado_view():
    if request.method == "POST":
        dni = int(request.form["dni"])
        pin = int(request.form["pin"])
        return registrar_empleado(dni,pin)
    
    return render_template("auth/registrar.html", mensaje=None)

@auth_bp.route("/logout_admin")
def logout_admin():
    session.clear()
    return render_template("auth/cerrar_sesion.html")
