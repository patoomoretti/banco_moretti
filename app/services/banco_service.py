from models.cliente import Cliente
from models.cuenta import Cuenta
from models.tarjetas import *
from models.prestamo import Prestamo
from utils.helpers import *
from flask import render_template
from datetime import datetime
import random
from database import db

def obtener_dashboard():
    clientes = Cliente.query.all()
    movimientos = Movimiento.query.all()

    total_clientes = len(clientes)
    hoy = datetime.now().strftime("%d-%m-%y")
    total_depositos_hoy = 0
    cant_transferencias_24h = 0

    for movimiento in movimientos:
        fecha_movimiento = movimiento.fecha.split()[0]

        if fecha_movimiento == hoy:
            if movimiento.tipo == "deposito":
                total_depositos_hoy += movimiento.monto
            elif movimiento.tipo == "transferencia":
                cant_transferencias_24h += 1

    ultimos_clientes = Cliente.query.order_by(Cliente.id.desc()).limit(3).all()

    return {"total_clientes": total_clientes,"total_depositos_hoy": total_depositos_hoy,"cant_transferencias_24h": cant_transferencias_24h,"ultimos_clientes": ultimos_clientes,"hoy": hoy,}


def alta_cliente(nombre, apellido, dni, direccion, piso, departamento, telefono, email):
    try:
        cliente = Cliente.query.filter_by(dni=dni).first()

        if cliente:
            return render_template("empleado/agregar_cliente.html", mensaje="⚠️ El cliente ya esta registrado.")
        
        nuevo_cliente = Cliente(
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            direccion=direccion,
            piso=piso,
            departamento=departamento,
            telefono=telefono,
            email=email
        )
        
        db.session.add(nuevo_cliente)
        db.session.commit()
        return render_template("empleado/agregar_cliente.html", mensaje="✅ Ha sido registrado correctamente")
    
    except Exception as e:
        db.session.rollback()
        return render_template("empleado/agregar_cliente.html", mensaje=f"❌ Error inesperado: {str(e)}")
     

def baja_cliente(dni):
    '''
    Baja del cliente solicitado
    '''
    try:
        cliente = Cliente.query.filter_by(dni=dni).first()
        if not cliente:
            return render_template("empleado/eliminar_cliente.html", mensaje="⚠️ El cliente no existe.")
        
        db.session.delete(cliente)
        db.session.commit()
        print("Cliente eliminado:", cliente)
        return render_template("empleado/eliminar_cliente.html", mensaje="✅ Cliente eliminado correctamente")
    except Exception as e:
        db.session.rollback()
        return render_template("empleado/eliminar_cliente.html", mensaje=f"❌ Error inesperado: {str(e)}")
        
        
def obtener_clientes():
    
    todos_los_clientes = Cliente.query.all()
    cuentas_clientes = Cuenta.query.all()
    
    for cliente in todos_los_clientes:
        cliente.numero = "Sin cuenta"
        for cuenta in cuentas_clientes:
            if cliente.dni == cuenta.dni:
                cliente.numero = cuenta.numero
                break
    
    return todos_los_clientes


def obtener_perfil_cliente(dni):
    
    cliente = Cliente.query.filter_by(dni=dni).first()
    cuenta = Cuenta.query.filter_by(dni=dni).first()
    movimientos = Movimiento.query.filter_by(dni=dni).all() # Devuelve todos los movimientos
    
    return {"cliente": cliente,"cuenta":cuenta,"movimientos": movimientos}


def modificar_datos_cliente(dni,direccion,piso,departamento,telefono,email):
    cliente = Cliente.query.filter_by(dni=dni).first()

    if cliente is None:
        return None
    
    cliente.direccion = direccion
    cliente.piso = piso
    cliente.departamento = departamento
    cliente.telefono = telefono
    cliente.email = email
    
    db.session.commit()
    return cliente
                

def buscar_cliente(dni):
    ''''
    Buscar el cliente por el numero de DNI
    '''
    try:
        cliente_encontrado = Cliente.query.filter_by(dni=dni).first()
        
        if not cliente_encontrado:
            return render_template("empleado/buscar_cliente.html", cliente=None, mensaje="❌ No se encuentra el cliente.")
        
        return render_template("empleado/buscar_cliente.html", cliente=cliente_encontrado, mensaje="✅ Cliente encontrado")
    except Exception as e:
        db.session.rollback()
        return render_template("empleado/buscar_cliente.html", cliente=None, mensaje=f"❌ Error inesperado: {str(e)}")


def alta_cuenta_cliente(dni, tipo_cuenta):
    '''
    Crea cuenta bancaria para el cliente que ya se encuentre registrado en el banco
    '''
    try:
        cliente = Cliente.query.filter_by(dni=dni).first()
        cuenta = Cuenta.query.filter_by(dni=dni,tipo_cuenta=tipo_cuenta).first()
        if not cliente:
            return render_template("empleado/alta_cuenta_cliente.html", mensaje="❌ El cliente no existe")
        
        if cuenta:
            return render_template("empleado/alta_cuenta_cliente.html", mensaje="⚠️ El cliente ya posee esa cuenta")

        id_cuenta = f"{random.randint(0, 999999):06d}"
        numero = id_cuenta

        nueva_cuenta = Cuenta(
            numero=numero,
            dni=dni,
            tipo_cuenta=tipo_cuenta,
            saldo= 0,
            saldo_dolar= None
        )

        db.session.add(nueva_cuenta)
        db.session.commit()
        return render_template("empleado/alta_cuenta_cliente.html", mensaje="✅ Cuenta creada exitosamente.")
    
    except Exception as e:
        db.session.rollback()
        return render_template("empleado/alta_cuenta_cliente.html", cliente=None, mensaje=f"❌ Error inesperado: {str(e)}")


def alta_producto(dni, marca, tipo_producto):
    '''
    Agregar un producto tarjeta si es visa/master o si es credito/debito
    '''
    try:
        cliente = Cliente.query.filter_by(dni=dni).first()
        tarjeta = Tarjeta.query.filter_by(dni=dni,marca=marca,tipo=tipo_producto).first()

        if not cliente:
            return render_template("empleado/alta_producto.html", mensaje="⚠️ El cliente no existe.")

        if tarjeta:
            return render_template("empleado/alta_producto.html", mensaje=f"⚠️ El cliente ya posee una {marca} {tipo_producto}.")

        numero = f"{random.randint(0, 9999):04d} - {random.randint(0, 9999):04d} - {random.randint(0, 9999):04d} - {random.randint(0, 9999):04d}"
        fecha_vencimiento = f"{random.randint(1, 12):02d} - {random.randint(27, 36):02d}"
        cvv = f"{random.randint(0, 999):03d}"

        nueva_tarjeta = Tarjeta(
            dni=dni,
            marca=marca,
            tipo=tipo_producto,
            numero= numero,
            fecha_vencimiento= fecha_vencimiento,
            cvv=cvv,
            consumos= 0.0,
            limite= 50000
        )

        db.session.add(nueva_tarjeta)
        db.session.commit()
        return render_template("empleado/alta_producto.html", mensaje="✅ Producto agregado correctamente.")
    
    except Exception as e:
        db.session.rollback()
        return render_template("empleado/alta_producto.html", mensaje=f"❌ Error inesperado: {str(e)}")
        

def obtener_productos_cliente(dni):
    '''
        Ingresamos DNI y obtenemos los productos que tiene
    '''

    cliente = Cliente.query.filter_by(dni=dni).first()
    tarjetas = Tarjeta.query.filter_by(dni=dni).all()

    if not cliente:
        return {"cliente": None,"dni_buscado": dni,"mensaje": "⚠️ El cliente no existe."}

    productos = {
        "credito_visa": None,
        "debito_visa": None,
        "credito_master": None,
        "debito_master": None
    }

    for tarjeta in tarjetas:
        clave = f"{tarjeta.tipo}_{tarjeta.marca}"
        productos[clave] = tarjeta

    return {"cliente": productos,"dni_buscado": dni,"mensaje": None}
    

def baja_producto(dni, producto):
    '''
        Se le da de baja a un producto deseado por el cliente. Tarjeta Credito Visa/Master y Tarjeta Debito Visa/Master
    '''
    
    try:
        tipo, marca = producto.split("_")
        cliente = Cliente.query.filter_by(dni=dni).first()
        tarjeta = Tarjeta.query.filter_by(dni=dni,tipo=tipo,marca=marca).first()

        if not cliente:
            return render_template("empleado/baja_producto.html",mensaje="⚠️ El cliente no existe.")

        if not tarjeta:
            return render_template("empleado/baja_producto.html",mensaje="⚠️ El cliente no posee esa tarjeta.")

        db.session.delete(tarjeta)
        db.session.commit()

        return render_template("empleado/baja_producto.html",mensaje="✅ Producto eliminado correctamente.")
    except Exception as e:
        db.session.rollback()
        return render_template("empleado/baja_producto.html",mensaje=f"❌ Error inesperado: {e}")


def solicitar_prestamo(dni, monto, cuotas, tasa_interes, destino):
    try:
        cliente = Cliente.query.filter_by(dni=dni).first()
        if not cliente:
            return render_template("empleado/solicitar_prestamo.html", mensaje="⚠️ El cliente no existe.")
        
        interes_total = monto * (tasa_interes / 100)
        total = monto + interes_total
        monto_cuota = total / cuotas
        fecha_solicitud = datetime.now().strftime("%d-%m-%y")
        
        nuevo_prestamo = Prestamo(
            dni=dni,
            monto_solicitado= monto,
            monto_cuota= monto_cuota,
            cuotas_totales= cuotas,
            cuotas_pagas= 0,
            tasa_interes= tasa_interes,
            motivo= destino,
            fecha_solicitud= fecha_solicitud,
            total=total,
        )
        
        db.session.add(nuevo_prestamo)
        db.session.commit()
        return render_template("empleado/solicitar_prestamo.html", mensaje="✅ El prestamo ha sido otorgado")
    except Exception as e:
        db.session.rollback()
        return render_template("empleado/solicitar_prestamo.html", mensaje=f"❌ Error inesperado: {str(e)}")
