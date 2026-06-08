from flask import Flask, render_template, session, redirect, url_for
from models.movimientos import Movimiento
from models.usuarios import Usuario
from models.cliente import Cliente
from models.empleado import Empleado
import json
from database import db


# CHEQUEAR TODO LO QUE ES REGISTRAR/LOGIN

def leer_json(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def buscar_dni(dni, ruta):
    '''
    Busca el dni y si no lo encuentra retorna None
    '''
    leer_cuenta = leer_json(ruta)
    cliente_encontrado = None
    for i, c in enumerate(leer_cuenta):
        if int(c["dni"]) == int(dni):
            cliente_encontrado = c
            indice = i
            break

    if not cliente_encontrado:
        return None, None

    return cliente_encontrado, indice


def registrar_cuenta(dni, pin):
    '''
    El cliente se puede registrar si es que no tiene una cuenta
    '''
    cuenta = Usuario.query.filter_by(dni=dni).first()

    if cuenta:
        return render_template("auth/registrar.html", mensaje="⚠️ Ese usuario ya existe.")

    nueva_cuenta = Usuario(
        dni=dni,
        pin= pin
    )
    db.session.add(nueva_cuenta)
    db.session.commit()
    return render_template("auth/registrar.html", mensaje="✅ Cuenta registrada con éxito.")

def registrar_empleado(dni,pin):
    '''
    Registramos al nuevo empleado
    '''
    empleado = Usuario.query.filter_by(dni=dni,role="empleado").first()

    if empleado:
        return render_template("auth/registrar.html", mensaje="⚠️ Ese empleado ya existe.")

    nueva_cuenta = Usuario(
        dni=dni,
        pin= pin,
        role="empleado"
    )
    
    db.session.add(nueva_cuenta)
    db.session.commit()
    return render_template("auth/registrar.html", mensaje="✅ Cuenta registrada con éxito.")


def loguear_cuenta(dni, pin):
    '''
    Iniciar sesión si existe el usuario.
    Si no existe, le pregunta si quiere crear un usuario.
    Además, se asegura de que haya solo una sesión activa.
    '''
    cuenta = Usuario.query.filter_by(dni=dni).first()
    
    if not dni:
        return render_template("auth/login.html", mensaje="⚠️ El DNI no se encuentra registrado.")

    if cuenta and cuenta.pin == pin:
        session['role'] = 'cliente'
        session['dni'] = dni
        return redirect(url_for('cliente.cliente_inicio'))
    else:
        return render_template("auth/login.html", mensaje="❌ DNI o PIN incorrectos.")


def loguear_cuenta_admin(dni, pin):
    admin = Usuario.query.filter_by(dni=dni,pin=pin,role="empleado").first()
    nombre_admin = Empleado.query.filter_by(dni=dni).first()
    
    if not admin:
        return render_template("auth/login_admin.html", mensaje="⚠️ El DNI no se encuentra registrado.")

    # nombre_empleado = nombre_admin.nombre

    if admin.pin == pin:
        session['role'] = 'empleado'
        # session['nombre'] = nombre_empleado
        session['admin_dni'] = dni
        return render_template("empleado/empleado.html")
    else:
        return render_template("auth/login_admin.html", mensaje="❌ DNI o PIN incorrectos.")



# Esto estoy haciendo ahora
def restablecer_pin(dni, pin, pin_reingresar):
    '''
    Si se olvido el PIN, puede restablecerlo. Ingresa el dni de la cuenta que desea cambiar
    '''
    cliente = Usuario.query.filter_by(dni=dni).first()

    if not cliente:
        return render_template("auth/restablecer.html", mensaje="⚠️ El usuario no existe.")
    
    if pin != pin_reingresar:
        return render_template("auth/restablecer.html", mensaje="❌ Los PIN no coinciden.")
    
    cliente.pin = pin_reingresar
    db.session.commit()
    return render_template("auth/restablecer.html", mensaje="✅ El PIN ha sido cambiado correctamente.")



# A CHEQUEAR ESTO
def ver_datos_tarjeta_visa(dni, ruta, ruta_nombre):
    leer_cuenta = leer_json(ruta)
    leer_nombre = buscar_dni(dni, ruta_nombre)

    dinero = leer_cuenta["saldo"]
    cliente = leer_nombre["nombre"]
    limite_disponible = leer_cuenta["tarjeta_credito_visa"]["limite"]
    consumos_total = leer_cuenta["tarjeta_credito"]["consumos"]
    dinero_disponible = limite_disponible - consumos_total

    return dinero, cliente, limite_disponible, consumos_total, dinero_disponible






def agregar_movimientos(dni, tipo, detalle, fecha, monto, nombre_lista):
    leer_movimientos = leer_json("banco_moretti/data/movimientos.json")
    nuevo_movimiento = Movimiento(tipo, detalle, fecha, monto)

    agregar_movimiento = {
        "tipo": nuevo_movimiento.tipo,
        "detalle": nuevo_movimiento.detalle,
        "fecha": nuevo_movimiento.fecha,
        "monto": nuevo_movimiento.monto
    }

    encontrado = False
    for cliente in leer_movimientos:
        if int(cliente["dni"]) == int(dni):
            if nombre_lista not in cliente:
                cliente[nombre_lista] = []

            cliente[nombre_lista].append(agregar_movimiento)
            encontrado = True
            break

    if not encontrado:
        leer_movimientos.append({
            "dni": int(dni),
            nombre_lista: [agregar_movimiento]
        })

    guardar_json("banco_moretti/data/movimientos.json", leer_movimientos)
    

def formatear(valor):
    try:
        return f"{float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "0,00"
        
        
def guardar_edicion_perfil(dni_original, datos_actualizados, ruta):
    leer_clientes = leer_json(ruta)
    
    encontrado = False
    for cliente in leer_clientes:
        if int(cliente['dni']) == dni_original:
            cliente['nombre'] = datos_actualizados['nombre']
            cliente['apellido'] = datos_actualizados['apellido']
            cliente['direccion'] = datos_actualizados['direccion']
            cliente['piso'] = datos_actualizados['piso']
            cliente['departamento'] = datos_actualizados['departamento']
            cliente['telefono'] = datos_actualizados['telefono']
            cliente['email'] = datos_actualizados['email']
            encontrado = True
            break

    if encontrado:
        guardar_json(ruta, leer_clientes)
        return True

    return False  
