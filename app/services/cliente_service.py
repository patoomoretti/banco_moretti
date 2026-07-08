from models.transferencia import Transferencia
from models.movimientos import Movimiento
from models.cuenta import Cuenta
from models.tarjetas import Tarjeta
from models.compra_tarjeta import CompraTarjeta
from models.prestamo import Prestamo
from datetime import datetime
from utils.helpers import *
from flask import render_template
from database import db


def depositar_dinero(dni, saldo):
    try:
        cuenta = Cuenta.query.filter_by(dni=dni).first()
        
        if not cuenta:
            return render_template("cliente/depositar_dinero.html", mensaje="⚠️ El cliente no existe.")
        
        if saldo <= 0:
            return render_template("cliente/depositar_dinero.html", mensaje="❌ Tiene que ser mayor que 0.")
        
        fecha_hoy = datetime.now().strftime("%d-%m-%y  %H:%M")
        
        cuenta.saldo += saldo
        
        nuevo_movimiento = Movimiento(
            dni=dni,
            tipo="Deposito",
            detalle="Deposito de dinero en cuenta",
            fecha=fecha_hoy,
            monto=saldo
        )
        
        db.session.add(nuevo_movimiento)
        db.session.commit()
        return render_template("cliente/depositar_dinero.html", mensaje="✅ Se ha depositado el dinero.")
    
    except Exception as e:
        db.session.rollback()
        return render_template("cliente/depositar_dinero.html", mensaje=f"❌ Error inesperado: {str(e)}")


def retirar_dinero(dni, monto):
    try:
        cuenta = Cuenta.query.filter_by(dni=dni).first()
        monto = float(monto)
        
        if not cuenta:
            return render_template("cliente/retirar_dinero.html", mensaje="⚠️ El cliente no existe.")
        
        if monto <= 0:
            return render_template("cliente/retirar_dinero.html", mensaje="❌ El monto tiene que ser mayor que 0.")
        
        if cuenta.saldo < monto:
            return render_template("cliente/retirar_dinero.html", mensaje="⚠️ Fondos insuficientes.")
        
        fecha_hoy = datetime.now().strftime("%d-%m-%y  %H:%M")
        cuenta.saldo -= monto
        
        nuevo_movimiento = Movimiento(
            dni=dni,
            tipo="Extraccion",
            detalle="Retiro de dinero en cuenta",
            fecha=fecha_hoy,
            monto=monto * -1
        )
        
        db.session.add(nuevo_movimiento)
        db.session.commit()
        return render_template("cliente/retirar_dinero.html", mensaje="✅ Retiro de dinero exitoso.")
    
    except Exception as e:
        db.session.rollback()
        return render_template("cliente/retirar_dinero.html", mensaje=f"❌ Error inesperado: {str(e)}")


def transferir_dinero(dni_origen, dni_destino, monto):
    '''
    Transferencia de dinero de una cuenta a otra verificando si existen las cuentas y que tenga saldo para poder hacerlo. Tambien se guarda cada transferencia realizada.
    '''
    try:
        cuenta_origen = Cuenta.query.filter_by(dni=dni_origen).first()
        cuenta_destino = Cuenta.query.filter_by(dni=dni_destino).first()
        fecha = datetime.now().strftime("%d-%m-%y  %H:%M")

        if cuenta_origen is None:
            return render_template("cliente/transferir_dinero.html", mensaje="⚠️ El DNI origen no existe.")
        elif cuenta_destino is None:
            return render_template("cliente/transferir_dinero.html", mensaje="⚠️ El DNI destino no existe.")
        
        if dni_origen == int(dni_destino):
            return render_template("cliente/transferir_dinero.html", mensaje="⚠️ No se puede transferir a uno mismo.")

        if monto <= 0:
            return render_template("cliente/transferir_dinero.html", mensaje="⚠️ El monto debe ser positivo.")
        if monto > cuenta_origen.saldo:
            return render_template("cliente/transferir_dinero.html", mensaje="❌ No cuenta con los fondos suficientes para hacer la transferencia.")

        tipo = "Transferencia"
        tipo_recibido = "Transferencia Recibida"
        detalle_env = f"Transferencia enviada a DNI {dni_destino}"
        detalle_rec = f"Transferencia recibida de DNI {dni_origen}"
        
        nueva_transferencia = Transferencia(
            dni_origen=dni_origen,
            dni_destino= dni_destino,
            monto= monto,
            fecha= fecha
        )
        
        nuevo_movimiento_origen = Movimiento(
            dni= dni_origen,
            tipo = tipo,
            detalle = detalle_env,
            fecha = fecha,
            monto = monto * -1
        )
        
        nuevo_movimiento_destino = Movimiento(
            dni = dni_destino,
            tipo = tipo_recibido,
            detalle = detalle_rec,
            fecha = fecha,
            monto = monto
        )

        cuenta_origen.saldo -= monto
        cuenta_destino.saldo += monto
        
        db.session.add(nueva_transferencia)
        db.session.add(nuevo_movimiento_origen)
        db.session.add(nuevo_movimiento_destino)
        db.session.commit()
        return render_template("cliente/transferir_dinero.html", mensaje="✅ Transferencia realizada.")
    
    except Exception as e:
        db.session.rollback()
        return render_template("cliente/transferir_dinero.html", mensaje=f"❌ Error inesperado: {str(e)}")


def solicitar_prestamo(dni,monto,destino,plazo):
    '''
        Simula un prestamo y si esta de acuerdo lo solicita
    '''
    try:
        prestamo = Prestamo.query.filter_by(dni=dni,estado="activo").first()
        
        if prestamo:
            return render_template("cliente/solicitar_prestamo.html", mensaje="⚠️ Ya posee un prestamo. ")
        
        if monto <= 0:
            return render_template("cliente/solicitar_prestamo.html", mensaje="❌ El monto debe ser mayor a 0.")

        if plazo == 12:
            tna = 0.45
        elif plazo == 24:
            tna = 0.55
        elif plazo == 36:
            tna = 0.65
        elif plazo == 48:
            tna = 0.75
        else:
            return render_template("cliente/solicitar_prestamo.html", mensaje="❌ Plazo no valido.")
                
        interes_total = monto * tna
        total = monto + interes_total
        monto_cuota = total / plazo

        ahora = datetime.now()

        mes_fin = ahora.month + plazo
        anio_fin = ahora.year

        while mes_fin > 12:
            mes_fin -= 12
            anio_fin += 1

        fecha_solicitud = ahora.strftime("%d-%m-%y")
        fecha_fin = f"{mes_fin:02d}-{anio_fin}"
        
        nuevo_prestamo = Prestamo(
            dni=dni,
            monto_solicitado=monto,
            monto_cuota=monto_cuota,
            cuotas_totales=plazo,
            cuotas_pagas=0,
            tasa_interes=tna,
            motivo=destino,
            fecha_solicitud=fecha_solicitud,
            total=total,
            estado="activo",
            fecha_fin=fecha_fin
        )
        
        db.session.add(nuevo_prestamo)
        db.session.commit()
        return render_template("cliente/solicitar_prestamo.html", mensaje="✅ Se ha enviado la solicitud")
    
    except Exception as e:
        db.session.rollback()
        return render_template("cliente/solicitar_prestamo.html", mensaje=f"❌ Error inesperado: {str(e)}")


def agregar_consumo_tarjeta(dni,producto, importe, cuotas, tipo_tarjeta):
    try:
    
        tarjeta = Tarjeta.query.filter_by(dni=dni,tipo=tipo_tarjeta).first()
        
        if tarjeta is None:
            return render_template("cliente/agregar_consumo.html", mensaje=f"❌ No tienes activa la tarjeta")

        if importe <= 0:
            return render_template("cliente/agregar_consumo.html", mensaje="❌ El importe debe ser mayor a cero.")

        intereses = 0
        if cuotas == 3:
            intereses = importe * 0.10
        elif cuotas == 6:
            intereses = importe * 0.20
        elif cuotas == 9:
            intereses = importe * 0.30

        importe_final = importe + intereses
        importe_cuotas = importe_final / cuotas

        tarjeta.consumos += importe_final

        ahora = datetime.now()
        periodo_actual = ahora.strftime("%Y-%m") 
        fecha_formateada = ahora.strftime("%d/%m/%Y")
        
        nuevo_consumo = CompraTarjeta(
            dni=dni,
            tarjeta_id= tarjeta.id,
            producto= producto,
            importe= round(importe_final, 2),
            importe_cuota= round(importe_cuotas, 2),
            cuotas_totales= cuotas,
            cuota_actual= 1,
            fecha= fecha_formateada,
            periodo= periodo_actual
        )
        
        db.session.add(nuevo_consumo)
        db.session.commit()
        return render_template("cliente/consumo_tarjeta.html", mensaje="✅ Compra realizada con exito.")
        
    except Exception as e:
        db.session.rollback()
        return render_template("cliente/consumo_tarjeta.html", mensaje=f"❌ Error inesperado: {str(e)}")
    

def pagar_tarjeta(marca, monto, dni, tipo_pago):
    try:
        cuenta = Cuenta.query.filter_by(dni=dni).first()
        tarjeta = Tarjeta.query.filter_by(dni=dni, tipo=marca).first()

        if not tarjeta or not tipo_pago:
            return render_template("cliente/pagar_tarjeta.html", mensaje="⚠️ Debes seleccionar tarjeta y tipo de pago.")

        if tarjeta.consumos <= 0:
            return render_template("cliente/pagar_tarjeta.html", mensaje="⚠️ No tiene consumos hechos")

        tipo_visa = "Pago Tarjeta Visa Credito"
        tipo_master = "Pago Tarjeta Master Credito"
        detalle_total = "Pago Total"
        detalle_parcial = "Pago Parcial"
        fecha = datetime.now().strftime("%d-%m-%y  %H:%M")
        deuda = tarjeta.consumos
        
        if marca == "visa":
            tipo_mov = tipo_visa
        else:
            tipo_mov = tipo_master

        if tipo_pago == "total":
            if cuenta.saldo < deuda:
                return render_template("cliente/pagar_tarjeta.html", mensaje="❌ No dispone de saldo suficiente.")
            cuenta.saldo -= deuda
            tarjeta.consumos = 0
            detalle = detalle_total
            monto_mov = deuda
        else:
            monto = float(monto)
            if monto > deuda:
                return render_template("cliente/pagar_tarjeta.html", mensaje="❌ No se puede pagar más del consumo actual.")
            if cuenta.saldo < monto:
                return render_template("cliente/pagar_tarjeta.html", mensaje="❌ No dispone de saldo suficiente.")
            cuenta.saldo -= monto
            tarjeta.consumos -= monto
            detalle = detalle_parcial
            monto_mov = monto

        nuevo_pago = Movimiento(
            dni=dni, 
            tipo=tipo_mov, 
            detalle=detalle, 
            fecha=fecha, 
            monto=monto_mov * -1
        )
        db.session.add(nuevo_pago)
        db.session.commit()
        return render_template("cliente/pagar_tarjeta.html", mensaje=f"✅ Pago de tarjeta {marca.upper()} realizado con éxito.")

    except Exception as e:
        db.session.rollback()
        return render_template("cliente/pagar_tarjeta.html", mensaje=f"❌ Error inesperado: {str(e)}")


def obtener_transferencias_cliente(dni):
    transferencias_finales = []
    enviadas = Transferencia.query.filter_by(dni_origen=dni).all()

    for t in enviadas:
        transferencia = {
            "dni_destino": t.dni_destino,
            "monto": t.monto,
            "fecha": t.fecha,
            "es_recepcion": False
        }

        transferencias_finales.append(transferencia)

    recibidas = Transferencia.query.filter_by(dni_destino=dni).all()

    for t in recibidas:
        transferencia = {
            "dni_origen": t.dni_origen,
            "monto": t.monto,
            "fecha": t.fecha,
            "es_recepcion": True
        }
        transferencias_finales.append(transferencia)

    transferencias_finales.sort(key=lambda x: x["fecha"],reverse=True)

    return transferencias_finales


def obtener_movimientos_cliente(dni):
    movimientos = Movimiento.query.filter_by(dni=dni).all()
    movimientos_lista = []

    for m in movimientos:
        movimiento = {
            "tipo": m.tipo,
            "detalle": m.detalle,
            "fecha": m.fecha,
            "monto": m.monto
        }
        movimientos_lista.append(movimiento)

    movimientos_lista.sort(key=lambda x: x["fecha"],reverse=True)
    return movimientos_lista
    