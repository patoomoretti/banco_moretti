from flask import Blueprint, render_template, request, redirect, session,flash
from services.cliente_service import *
from models.cliente import Cliente
from models.cuenta import Cuenta
from models.tarjetas import Tarjeta
from utils.helpers import formatear
from utils.decorators import login_required,cliente_required

cliente_bp = Blueprint("cliente", __name__)


@cliente_bp.route("/cliente/inicio", methods=["GET"])
@cliente_required 
def cliente_inicio():
    dni = session.get("dni")
    
    cliente = Cliente.query.filter_by(dni=dni).first() 
    cuenta = Cuenta.query.filter_by(dni=dni).first() 
    tarjeta_v_c = Tarjeta.query.filter_by(dni=dni, marca="visa", tipo="credito").first()
    tarjeta_v_d = Tarjeta.query.filter_by(dni=dni, marca="visa", tipo="debito").first()
    tarjeta_m_c = Tarjeta.query.filter_by(dni=dni, marca="master", tipo="credito").first()
    tarjeta_m_d = Tarjeta.query.filter_by(dni=dni, marca="master", tipo="debito").first()
    
    if not cliente or not cuenta:
        return redirect("/login")
    nombre_cliente = cliente.nombre
    
    saldo_formateado_pesos = formatear(cuenta.saldo)
    saldo_formateado_dolar= formatear(cuenta.saldo_dolar or 0)
    
    visa_credito_disponible = "0,00"
    visa_credito_limite = "0,00"
    visa_debito_disponible = "0,00"
    visa_debito_limite = "0,00"
    master_credito_disponible = "0,00"
    master_credito_limite = "0,00"
    master_debito_disponible = "0,00"
    master_debito_limite = "0,00"
    
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
@cliente_required
def depositar():
    dni = session.get("dni")
    if request.method == "POST":
        saldo = int(request.form["saldo",0])
        return depositar_dinero(dni, saldo)

    return render_template("cliente/depositar_dinero.html", mensaje=None)


@cliente_bp.route("/cliente/retirar_dinero", methods=["GET","POST"])
@cliente_required
def retirar():
    dni = session.get("dni")
    if request.method == "POST":
        monto = request.form.get("monto")
        return retirar_dinero(dni,monto)
        
    return render_template("cliente/retirar_dinero.html", mensaje=None)


@cliente_bp.route("/cliente/transferir_dinero", methods=["GET", "POST"])
@cliente_required
def transferir_view():
    dni = session.get("dni")
    if request.method == "POST":
        dni_destino = request.form.get("dni_destino")
        monto = int(request.form.get("monto"))
        return transferir_dinero(dni, dni_destino, monto)

    return render_template("cliente/transferir_dinero.html", mensaje=None)


# hacer este
@cliente_bp.route("/cliente/solicitar_prestamo",methods=["GET","POST"])
@cliente_required
def solicitar_prestamo_view():
    dni = session.get("dni")
    
    if request.method == "POST":
        monto = int(request.form.get("monto"))
        destino = request.form.get("destino")
        plazo = request.form.get("plazo")
        return solicitar_prestamo(dni,monto,destino,plazo)
     
    return render_template("cliente/solicitar_prestamo.html",mensaje=None)


@cliente_bp.route("/cliente/pagar_tarjeta", methods=["GET", "POST"])
@cliente_required
def pagar():
    dni = session.get("dni")

    if request.method == "POST":
        tipo_pago = request.form.get("tipo_pago", "total")
        tarjeta = request.form.get("tarjeta")
        monto = request.form.get("monto")
        return pagar_tarjeta(tarjeta, monto, dni, tipo_pago)

    visa = Tarjeta.query.filter_by(dni=dni, marca="visa", tipo="credito").first()
    master = Tarjeta.query.filter_by(dni=dni, marca="master", tipo="credito").first()

    deuda_visa = 0
    deuda_master = 0

    if visa:
        deuda_visa = visa.consumos
    if master:
        deuda_master = master.consumos

    return render_template("cliente/pagar_tarjeta.html",
        mensaje=None,deuda_visa=deuda_visa,deuda_master=deuda_master)


@cliente_bp.route("/cliente/consumo_tarjeta", methods=["GET","POST"])
@cliente_required
def agregar_consumo():
    dni = session.get("dni")
    cuenta = Tarjeta.query.filter_by(dni=dni).first()
    
    visa_c = Tarjeta.query.filter_by(dni=dni,marca="visa",tipo="credito").first()
    visa_d = Tarjeta.query.filter_by(dni=dni,marca="visa",tipo="debito").first()
    master_c = Tarjeta.query.filter_by(dni=dni,marca="master",tipo="credito").first()
    master_d = Tarjeta.query.filter_by(dni=dni,marca="master",tipo="debito").first()
    if request.method == "POST":
        producto = request.form.get("producto")
        importe = float(request.form.get("importe"))
        cuotas = int(request.form.get("cuotas"))
        tipo_tarjeta = request.form.get("tipo_tarjeta")
        agregar_consumo_tarjeta(dni, producto, importe, cuotas, tipo_tarjeta)
    
    return render_template("cliente/agregar_consumo.html", visa_c=visa_c,visa_d=visa_d,master_c=master_c,master_d=master_d)


# Cambiar a base de datos
@cliente_bp.route("/cliente/resumen_tarjeta", methods=["GET", "POST"])
@cliente_required
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
@cliente_required
def ver_transferencias():
    dni = session.get("dni")
    transferencias = obtener_transferencias_cliente(dni)

    return render_template("cliente/transferencias.html",transferencias=transferencias)
    
    
@cliente_bp.route("/cliente/movimientos", methods=["GET"])
@cliente_required
def movimientos_completos():
    dni = session.get("dni")
    movimientos = obtener_movimientos_cliente(dni)

    return render_template("cliente/movimientos.html",movimientos=movimientos)