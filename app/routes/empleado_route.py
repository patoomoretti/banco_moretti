from flask import Blueprint, render_template,redirect,session,url_for,request
from services.banco_service import * 
from utils.helpers import *
from datetime import datetime

empleado_bp = Blueprint("empleado", __name__)

@empleado_bp.route('/menu',methods=["GET","POST"])
def empleado_inicio():
    if session.get('role') != 'empleado':
        return redirect(url_for('auth.login_admin')) # Si un cliente intenta entrar, lo manda al login
    
    return render_template('empleado/empleado.html', nombre=session.get('nombre'))


@empleado_bp.route("/dashboard")
def dashboard_empleado():
    clientes = leer_json("banco_moretti/data/clientes.json")
    movimientos_data = leer_json("banco_moretti/data/movimientos.json")
    
    total_clientes = len(clientes)
    hoy = datetime.now().strftime("%d-%m-%y")
    total_depositos_hoy = 0
    cant_transferencias_24h = 0
    
    for registro in movimientos_data:
        
        # Sumar depósitos si la fecha es hoy
        if 'deposito' in registro:
            for d in registro['deposito']:
                fecha_movimiento = d['fecha'].split()[0]
                if fecha_movimiento == hoy:
                    total_depositos_hoy = total_depositos_hoy + d['monto']
        
        # Contar transferencias si la fecha es hoy
        if 'transferencia' in registro:
            for t in registro['transferencia']:
                fecha_movimiento = t['fecha'].split()[0]
                if fecha_movimiento == hoy:
                    cant_transferencias_24h = cant_transferencias_24h + 1

    # ultimos 3 clientes
    ultimos_clientes = clientes[-3:] 
    ultimos_clientes.reverse()

    return render_template("empleado/dashboard.html",total_clientes=total_clientes,total_depositos_hoy=total_depositos_hoy,cant_transferencias_24h=cant_transferencias_24h,ultimos_clientes=ultimos_clientes,hoy=hoy)
    
    
@empleado_bp.route("/buscar_cliente", methods=["GET","POST"])
def buscar_cliente_view():    
    if request.method == "POST":
        dni = int(request.form.get("dni_busqueda"))
        return buscar_cliente(dni)
        
    return render_template("empleado/buscar_cliente.html",mensaje=None,cliente=None)
    
# actualizado con base de datos
@empleado_bp.route("/alta_cliente", methods=["GET","POST"])
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
def eliminar_cliente_view():
    if request.method == "POST":
        dni = int(request.form.get("dni"))
        return baja_cliente(dni)
        
    return render_template("empleado/eliminar_cliente.html",mensaje=None)
        

@empleado_bp.route("/datos_cliente")
def datos_cliente():
    ruta = "banco_moretti/data/clientes.json"
    ruta_cuenta = "banco_moretti/data/cuentas_bancarias.json"
    todos_los_clientes = leer_json(ruta)
    cuentas_clientes = leer_json(ruta_cuenta)
    
    for c in todos_los_clientes:
        c['numero'] = "Sin cuenta"
        for n in cuentas_clientes:
            if int(c['dni']) == int(n['dni']):
                c['numero'] = n['numero']
    
    return render_template("empleado/datos_cliente.html", clientes=todos_los_clientes)

@empleado_bp.route("/perfil_cliente/<int:dni>")
def perfil_cliente(dni):
    ruta = "banco_moretti/data/clientes.json"
    ruta_movimientos = "banco_moretti/data/movimientos.json"
    
    cliente_encontrado, _ = buscar_dni(dni, ruta)
    todos_los_movimientos = leer_json(ruta_movimientos)
    
    movimientos_unificados = []
    for registro in todos_los_movimientos:
        if int(registro['dni']) == int(dni):
            categorias = ['transferencia', 'pago_tarjeta_visa', 'pago_tarjeta_master', 'deposito', 'extraccion']
            
            for cat in categorias:
                if cat in registro: 
                    for movimiento in registro[cat]:
                        movimientos_unificados.append(movimiento)
    
    # Ordenado por fecha. Del reciente al mas antiguo
    movimientos_unificados.sort(key=lambda x: x['fecha'], reverse=True)
    
    return render_template("empleado/perfil_cliente.html",cliente=cliente_encontrado,movimientos=movimientos_unificados)

@empleado_bp.route("/actualizar_cliente", methods=["POST"])
def actualizar_cliente():
    ruta = "banco_moretti/data/clientes.json"
    dni_original = int(request.form.get("dni_original"))

    datos_actualizados = {
        "nombre": request.form.get("nombre"),
        "apellido": request.form.get("apellido"),
        "direccion": request.form.get("direccion"),
        "piso": request.form.get("piso") ,
        "departamento":request.form.get("departamento") ,
        "telefono": request.form.get("telefono"),
        "email": request.form.get("email")
    }

    guardar_edicion_perfil(dni_original, datos_actualizados, ruta)
    
    return redirect(url_for('empleado.datos_cliente'))


@empleado_bp.route("/alta_cuenta_cliente", methods=["POST","GET"])
def crear_cuenta_view():
    if request.method == "POST":
        dni = int(request.form.get("dni"))
        tipo_cuenta = str(request.form.get("tipo_cuenta"))
        return alta_cuenta_cliente(dni,tipo_cuenta)
        
    return render_template("empleado/alta_cuenta_cliente.html",mensaje=None)


@empleado_bp.route("/alta_producto", methods=["POST","GET"])
def alta_producto_view():
    if request.method == "POST":
        dni = int(request.form.get("dni"))
        marca = str(request.form.get("marca"))
        tipo_producto = str(request.form.get("tipo_producto"))
        return alta_producto(dni,marca,tipo_producto)
    
    return render_template("empleado/alta_producto.html",mensaje=None)


@empleado_bp.route("/baja_producto", methods=["GET", "POST"])
def baja_producto_view():
    ruta = "banco_moretti/data/cuentas_bancarias.json"
    cliente_encontrado = None
    dni_buscado = None

    if request.method == "POST":
        dni_buscado = request.form.get("dni")
        cliente_encontrado, indice = buscar_dni(dni_buscado, ruta)

    return render_template("empleado/baja_producto.html",cliente=cliente_encontrado,dni_buscado=dni_buscado)

@empleado_bp.route("/confirmar_baja_producto", methods=["POST","GET"])
def confirmar_baja_view():
    if request.method == "POST":
        dni = int(request.form.get("dni"))
        tipo_producto = str(request.form.get("producto_baja"))
        return baja_producto(dni,tipo_producto)
    
    return render_template("empleado/baja_producto.html",mensaje=None)


@empleado_bp.route("/solicitar_prestamo",methods=["GET","POST"])
def solicitar_prestamo_view():
    fecha_solicitud = datetime.now().strftime("%d-%m-%y")
    
    if request.method == "POST":
        dni = int(request.form.get("dni"))
        monto = int(request.form.get("monto"))
        cuotas = int(request.form.get("cuotas"))
        tasa_interes = int(request.form.get("tasa"))
        motivo = str(request.form.get("destino"))
        
        return solicitar_prestamo(dni,monto,cuotas,tasa_interes,motivo,fecha_solicitud)
        
    return render_template("empleado/solicitar_prestamo.html",mensaje=None,hoy=fecha_solicitud)
