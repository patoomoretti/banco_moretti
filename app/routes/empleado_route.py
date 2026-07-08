from flask import Blueprint, render_template,redirect,session,url_for,request
from services.banco_service import * 
from utils.helpers import *
from datetime import datetime
from utils.decorators import login_required,empleado_required 

empleado_bp = Blueprint("empleado", __name__)

@empleado_bp.route('/menu',methods=["GET","POST"])
@empleado_required
def empleado_inicio():

    return render_template('empleado/empleado.html', nombre=session.get('nombre'))


@empleado_bp.route("/dashboard")
@empleado_required
def dashboard_empleado():    
    datos = obtener_dashboard()
    return render_template("empleado/dashboard.html",**datos)
    
    
@empleado_bp.route("/buscar_cliente", methods=["GET","POST"])
@empleado_required
def buscar_cliente_view():    
    if request.method == "POST":
        dni = int(request.form.get("dni_busqueda"))
        return buscar_cliente(dni)
        
    return render_template("empleado/buscar_cliente.html",mensaje=None,cliente=None)
    

@empleado_bp.route("/alta_cliente", methods=["GET","POST"])
@empleado_required
def agregar_nuevo_cliente():
    if request.method == "POST":
        nombre = str(request.form.get("nombre"))
        apellido = str(request.form.get("apellido"))
        dni = int(request.form.get("dni"))
        direccion = str(request.form.get("direccion"))
        piso = str(request.form.get("piso"))
        departamento = str(request.form.get("departamento"))
        telefono = int(request.form.get("telefono"))
        email = str(request.form.get("email"))
        
        return alta_cliente(nombre,apellido,dni,direccion,piso,departamento,telefono,email)
    
    return render_template("empleado/agregar_cliente.html",mensaje=None,nombre=session.get('nombre'))


@empleado_bp.route("/baja_cliente",methods=["GET","POST"])
@empleado_required
def eliminar_cliente_view():
    if request.method == "POST":
        dni = int(request.form.get("dni"))
        return baja_cliente(dni)
        
    return render_template("empleado/eliminar_cliente.html",mensaje=None)
        

@empleado_bp.route("/datos_cliente")
@empleado_required
def datos_cliente():
    clientes = obtener_clientes()
    return render_template("empleado/datos_cliente.html", **clientes)


@empleado_bp.route("/perfil_cliente/<int:dni>")
@empleado_required
def perfil_cliente(dni):
    perfil = obtener_perfil_cliente(dni)
    return render_template("empleado/perfil_cliente.html", clientes=perfil)
    

@empleado_bp.route("/actualizar_cliente", methods=["POST"])
@empleado_required
def actualizar_cliente():
    
    datos = {
    "dni": request.form.get("dni"),
    "direccion": request.form.get("direccion"),
    "piso": request.form.get("piso"),
    "departamento": request.form.get("departamento"),
    "telefono": request.form.get("telefono"),
    "email": request.form.get("email"),
    }
    modificar_datos_cliente(**datos)
        
    return redirect(url_for('empleado.datos_cliente'))


@empleado_bp.route("/alta_cuenta_cliente", methods=["POST","GET"])
@empleado_required
def crear_cuenta_view():
    if request.method == "POST":
        dni = int(request.form.get("dni"))
        tipo_cuenta = str(request.form.get("tipo_cuenta"))
        return alta_cuenta_cliente(dni,tipo_cuenta)
        
    return render_template("empleado/alta_cuenta_cliente.html",mensaje=None)


@empleado_bp.route("/alta_producto", methods=["POST","GET"])
@empleado_required
def alta_producto_view():
    if request.method == "POST":
        dni = int(request.form.get("dni"))
        marca = str(request.form.get("marca"))
        tipo_producto = str(request.form.get("tipo_producto"))
        return alta_producto(dni,marca,tipo_producto)
    
    return render_template("empleado/alta_producto.html",mensaje=None)


# aca estoy haciendo ahora. ACA ME QUEDE
@empleado_bp.route("/baja_producto", methods=["GET", "POST"])
@empleado_required
def baja_producto_view():
    
    if request.method == "POST":
        dni = int(request.form.get("dni"))
        tipo_producto = str(request.form.get("producto_baja"))             
        baja_producto(dni,tipo_producto)

    return render_template("empleado/baja_producto.html",mensaje=None)


@empleado_bp.route("/confirmar_baja_producto", methods=["POST","GET"])
@empleado_required
def confirmar_baja_view():
    if request.method == "POST":
        dni = int(request.form.get("dni"))
        tipo_producto = str(request.form.get("producto_baja"))
        return baja_producto(dni,tipo_producto)
    
    return render_template("empleado/baja_producto.html",mensaje=None)


@empleado_bp.route("/solicitar_prestamo",methods=["GET","POST"])
@empleado_required
def solicitar_prestamo_view():
    
    if request.method == "POST":
        dni = int(request.form.get("dni"))
        monto = int(request.form.get("monto"))
        cuotas = int(request.form.get("cuotas"))
        tasa_interes = int(request.form.get("tasa"))
        motivo = str(request.form.get("destino"))
        
        return solicitar_prestamo(dni,monto,cuotas,tasa_interes,motivo)
        
    return render_template("empleado/solicitar_prestamo.html",mensaje=None)
