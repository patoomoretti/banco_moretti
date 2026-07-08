from flask import Flask, render_template, session, redirect, url_for
from models.movimientos import Movimiento
from models.usuarios import Usuario
from models.cliente import Cliente
from models.empleado import Empleado
import json
from database import db


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

    nombre_empleado = nombre_admin.nombre

    if admin.pin == pin:
        session['role'] = 'empleado'
        session['nombre'] = nombre_empleado
        session['admin_dni'] = dni
        return render_template("empleado/empleado.html")
    else:
        return render_template("auth/login_admin.html", mensaje="❌ DNI o PIN incorrectos.")


def restablecer_pin(dni, pin, pin_reingresar):
    '''
    Si se olvido el PIN, puede restablecerlo. Ingresa el dni de la cuenta que desea cambiar
    '''
    try:
        cliente = Usuario.query.filter_by(dni=dni).first()
        if not cliente:
            return render_template("auth/restablecer.html", mensaje="⚠️ El usuario no existe.")
        
        if pin != pin_reingresar:
            return render_template("auth/restablecer.html", mensaje="❌ Los PIN no coinciden.")
        
        cliente.pin = pin_reingresar
        db.session.commit()
        return render_template("auth/restablecer.html", mensaje="✅ El PIN ha sido cambiado correctamente.")
    except Exception:
        db.session.rollback()
        return render_template("auth/restablecer.html", mensaje="❌ No ha sido posible cambiar el pin.")


def formatear(valor):
    try:
        return f"{float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "0,00"
        
        