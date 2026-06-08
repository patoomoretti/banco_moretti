from flask import Blueprint, render_template, request, redirect, session,flash
from services.cliente_service import *
from models.cliente import Cliente
from utils.helpers import formatear

cliente_bp = Blueprint("cliente", __name__)


@cliente_bp.route("/cliente/inicio", methods=["GET"])
def cliente_inicio():
    dni = session.get("dni")
    if not dni:
        return redirect("/login")
    
    cliente = Cliente.query.filter_by(dni=dni).first() 
    cuenta = Cuenta.query.filter_by(dni=dni).first() 
    tarjeta_v_c = Tarjeta.query.filter_by(dni=dni, marca="visa", tipo="credito").first()
    tarjeta_v_d = Tarjeta.query.filter_by(dni=dni, marca="visa", tipo="debito").first()
    tarjeta_m_c = Tarjeta.query.filter_by(dni=dni, marca="master", tipo="credito").first()
    tarjeta_m_d = Tarjeta.query.filter_by(dni=dni, marca="master", tipo="debito").first()
    
    nombre_cliente = cliente.nombre
    
    saldo_formateado_pesos = formatear(cuenta.saldo)
    saldo_formateado_dolar= formatear(cuenta.saldo_dolar or 0)
    
    visa_credito_disponible = visa_credito_limite = "0,00"
    visa_debito_disponible = visa_debito_limite = "0,00"
    master_credito_disponible = master_credito_limite = "0,00"
    master_debito_disponible = master_debito_limite = "0,00"
    
    
    if tarjeta_v_c:
        disponible_credito_visa = tarjeta_v_c.limite - tarjeta_v_c.consumos
        visa_credito_disponible = formatear(disponible_credito_visa)
        visa_credito_limite = formatear(tarjeta_v_c.limite)
        
    if tarjeta_v_d:
        disponible_debito_visa = tarjeta_v_d.limite - tarjeta_v_d.consumos
        visa_debito_disponible = formatear(disponible_debito_visa)
        visa_debito_limite = formatear(tarjeta_v_d.limite)

    if tarjeta_m_c:
        disponible_credito_master = tarjeta_m_c.limite - tarjeta_m_c.consumos
        master_credito_disponible = formatear(disponible_credito_master)
        master_credito_limite = formatear(tarjeta_m_c.limite)
        
    if tarjeta_m_d:
        disponible_debito_master = tarjeta_m_d.limite - tarjeta_m_d.consumos
        master_debito_disponible = formatear(disponible_debito_master)
        master_debito_limite = formatear(tarjeta_m_d.limite)
    

    return render_template("cliente/usuario.html", nombre=nombre_cliente, saldo_disponible=saldo_formateado_pesos,saldo_disponible_dolar=saldo_formateado_dolar,visa_credito_disponible=visa_credito_disponible,visa_credito_limite=visa_credito_limite,visa_debito_disponible=visa_debito_disponible,visa_debito_limite=visa_debito_limite,master_credito_disponible=master_credito_disponible,master_credito_limite=master_credito_limite,master_debito_disponible=master_debito_disponible,master_debito_limite=master_debito_limite,visa_credito=tarjeta_v_c,
    visa_debito=tarjeta_v_d,
    master_credito=tarjeta_m_c,
    master_debito=tarjeta_m_d)


@cliente_bp.route("/cliente/depositar_dinero", methods=["GET", "POST"])
def depositar():
    dni = session.get("dni")
    
    if request.method == "POST":
        saldo = int(request.form["saldo"])
        return depositar_dinero(dni, saldo)

    return render_template("cliente/depositar_dinero.html", mensaje=None)


@cliente_bp.route("/cliente/retirar_dinero", methods=["GET","POST"])
def retirar():
    dni = session.get("dni")
    if request.method == "POST":
        monto = request.form.get("monto")
        return retirar_dinero(dni,monto)
        
    return render_template("cliente/retirar_dinero.html", mensaje=None)


@cliente_bp.route("/cliente/transferir_dinero", methods=["GET", "POST"])
def transferir_view():
    dni = int(session.get("dni"))
    if request.method == "POST":
        dni_destino = int(request.form.get("dni_destino"))
        monto = int(request.form.get("monto"))
        return transferir_dinero(dni, dni_destino, monto)

    return render_template("cliente/transferir_dinero.html", mensaje=None)


# hacer este
@cliente_bp.route("/cliente/solicitar_prestamo",methods=["GET","POST"])
def solicitar_prestamo_view():
    dni = session.get("dni")
    
    if request.method == "POST":
        monto = int(request.form.get("monto"))
        destino = str(request.form.get("destino"))
        plazo = request.form.get("plazo")
        return solicitar_prestamo(dni,monto,destino,plazo)
     
    return render_template("cliente/solicitar_prestamo.html",mensaje=None)


@cliente_bp.route("/cliente/pagar_tarjeta", methods=["GET", "POST"])
def pagar():
    dni = session.get("dni")

    if request.method == "POST":
        tipo_pago = request.form.get("tipo_pago", "total")
        tarjeta = request.form.get("tarjeta")
        monto = request.form.get("monto")
        return pagar_tarjeta(tarjeta, monto, dni, tipo_pago)

    visa = Tarjeta.query.filter_by(dni=dni, marca="visa").first()
    master = Tarjeta.query.filter_by(dni=dni, marca="master").first()

    deuda_visa = 0
    deuda_master = 0

    if visa:
        deuda_visa = visa.consumos
    if master:
        deuda_master = master.consumos

    return render_template("cliente/pagar_tarjeta.html",
        mensaje=None,deuda_visa=deuda_visa,deuda_master=deuda_master)


@cliente_bp.route("/cliente/consumo_tarjeta", methods=["GET","POST"])
def agregar_consumo():
    dni = session.get("dni")
    cuenta = Tarjeta.query.filter_by(dni=dni).filter_by()
    
    visa_c = cuenta.get("tarjeta_credito_visa")
    visa_d = cuenta.get("tarjeta_debito_visa")
    master_c = cuenta.get("tarjeta_credito_master")
    master_d = cuenta.get("tarjeta_debito_master")
    
    
    if request.method == "POST":
        producto = request.form.get("producto")
        importe = float(request.form.get("importe"))
        cuotas = int(request.form.get("cuotas"))
        tipo_tarjeta = request.form.get("tipo_tarjeta")
        agregar_consumo_tarjeta(dni, producto, importe, cuotas, tipo_tarjeta)
    
    return render_template("cliente/agregar_consumo.html", visa_c=visa_c,visa_d=visa_d,master_c=master_c,master_d=master_d)


# QUEDA CHEQUEAR
@cliente_bp.route("/cliente/resumen_tarjeta", methods=["GET", "POST"])
def resumen_tarjeta():
    ruta_consumos = "banco_moretti/data/consumos_tarjeta_credito.json"
    ruta_cuenta = "banco_moretti/data/cuentas_bancarias.json"
    dni = session.get("dni")
    
    periodos_disponibles = obtener_periodos_disponibles()
    cuenta, indice = buscar_dni(dni, ruta_cuenta)

    visa_c = cuenta.get("tarjeta_credito_visa")
    visa_d = cuenta.get("tarjeta_debito_visa") 
    master_c = cuenta.get("tarjeta_credito_master") 
    master_d = cuenta.get("tarjeta_debito_master")

    resultado = None
    if request.method == "POST":
        tarjeta = request.form.get("tarjeta_id")
        periodo = request.form.get("periodo")
        resultado = generar_resumen(dni, ruta_consumos, tarjeta, periodo)

    return render_template("cliente/resumen.html",periodos=periodos_disponibles,resultado=resultado,visa_c=visa_c, visa_d=visa_d,master_c=master_c, master_d=master_d)
    

@cliente_bp.route("/cliente/transferencias")
def ver_transferencias():
    ruta = "banco_moretti/data/transferencias.json"
    dni_sesion = session.get('dni')

    todos_los_datos = leer_json(ruta)
    transferencias_finales = []

    for usuario in todos_los_datos:
        if usuario["dni"] == dni_sesion:
            for t in usuario.get("transferencia", []):
                t["es_recepcion"] = False
                transferencias_finales.append(t)
        else:
            for t in usuario.get("transferencia", []):
                if t["dni_destino"] == dni_sesion:
                    t_recibida = t.copy()
                    t_recibida["es_recepcion"] = True
                    t_recibida["dni_origen"] = usuario["dni"]
                    transferencias_finales.append(t_recibida)

    transferencias_finales.sort(key=lambda x: datetime.strptime(x['fecha'], "%d-%m-%y  %H:%M"), reverse=True)

    return render_template("cliente/transferencias.html", transferencias=transferencias_finales)
    
    
@cliente_bp.route("/cliente/movimientos", methods=["GET", "POST"])
def movimientos_completos():
    ruta = "banco_moretti/data/movimientos.json"
    dni = session.get('dni')
    datos_cliente, indice = buscar_dni(dni, ruta)
    todos_los_movimientos = []
    
    # 2. Definimos las llaves que contienen listas de movimientos
    categorias = ["transferencia", "pago_tarjeta_visa", "pago_tarjeta_master", "deposito", "extraccion"]

    for cat in categorias:
        if cat in datos_cliente:
            todos_los_movimientos.extend(datos_cliente[cat])

    todos_los_movimientos.sort(key=lambda x: datetime.strptime(x['fecha'], "%d-%m-%y  %H:%M"), reverse=True)
    
    return render_template("cliente/movimientos.html", movimientos=todos_los_movimientos)