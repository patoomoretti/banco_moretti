from models.usuario import Usuario
import json
        
        
def leer_json(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    

def guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)
        
    
def buscar_dni(dni,ruta):
    '''
    Busca el dni y si no lo encuentra retorna None
    '''
    leer_cuenta = leer_json(ruta)        
    cliente_encontrado = None
    for i,c in enumerate(leer_cuenta):
        if int(c["dni"]) == dni:
            cliente_encontrado = c
            indice = i
            break
            
    if not cliente_encontrado:
        print("----- No ha sido posible encontrar el DNI -----")
        return None, None
    
    return cliente_encontrado, indice
        

def registrar_cuenta(ruta):
    '''
    El cliente se puede registrar si es que no tiene una cuenta
    '''
    print("------------------------")
    print("REGISTRARSE")
    print("------------------------")
    
    # Leer las cuentas actuales
    cuentas = leer_json(ruta)
    
    # Pedir datos al usuario
    nuevo_dni = int(input("Ingrese el DNI: "))
    nuevo_pin = int(input("Ingrese el PIN: "))
    
    # Buscar si el DNI ya existe
    cliente, indice = buscar_dni(nuevo_dni, ruta)
    
    # Si el DNI existe, avisar que ya está registrado
    if cliente is not None:
        print("------------------------")
        print("La cuenta ya se encuentra registrada.")
        print("------------------------")
        return
    
    # Crear nueva cuenta
    nueva_cuenta = {
        "dni": nuevo_dni,
        "pin": nuevo_pin
    }
    
    # Agregar y guardar
    cuentas.append(nueva_cuenta)
    guardar_json(ruta, cuentas)
    
    print("------------------------")
    print("Cuenta registrada correctamente.")
    print("------------------------")
    
    
def loguear_cuenta(ruta):
    '''
    Iniciar sesión si existe el usuario. 
    Si no existe, le pregunta si quiere crear un usuario. 
    Además, se asegura de que haya solo una sesión activa.
    '''
    print("------------------------")
    print("INICIAR SESION")
    print("------------------------")

    leer_sesion = leer_json("data/sesion_actual.json")

    # Verificamos si ya hay una sesión activa
    if len(leer_sesion) > 0:
        print(f"Ya hay una sesión iniciada con el DNI: {leer_sesion[0]['dni']}")
        print("Debe cerrar la sesión actual antes de iniciar otra.")
        print("------------------------")
        return

    dni = int(input("Ingrese el DNI: "))
    pin = int(input("Ingrese el PIN: "))

    cuenta, indice = buscar_dni(dni, ruta)

    if not cuenta:
        print("El DNI no se encuentra registrado.")
        crear_cuenta = input("Desea crear una cuenta (si/no): ").lower()
        if crear_cuenta == "si":
            return registrar_cuenta()
        else:
            opcion = input("Elija qué desea hacer (iniciar sesion (is) / salir (s) ): ").lower()
            if opcion == "is":
                return loguear_cuenta(ruta)
            else:
                print("Saliendo del sistema...")
                return

    # Si el usuario existe, verificamos el PIN
    if int(cuenta["pin"]) == pin:
        nueva_sesion = {"dni": dni}
        leer_sesion.append(nueva_sesion)
        guardar_json("data/sesion_actual.json", leer_sesion)
        print("Logueo exitoso.")
        print("------------------------")
        return cuenta
    else:
        print("PIN incorrecto. Intente nuevamente.")
        return loguear_cuenta(ruta)
        

def sesion_actual():
    '''
    Mantiene la sesion iniciada para realizar operaciones. Verificamos si hay una sesion
    '''
    leer_sesion = leer_json("data/sesion_actual.json")
    dni = leer_sesion[0]["dni"]
    
    if not dni:
        print("No has iniciado sesion.")
        iniciar_sesion = input("Desea iniciar sesion? (s/n): ")
        if iniciar_sesion == "s":
            return loguear_cuenta()
        else:
            print("La sesion sigue abierta.")
            leer_sesion.remove(dni)
            return
    
    
def cerrar_sesion(ruta):
    '''
    Se eliminan los datos de inicio de sesion y no puede operar
    '''
    leer_sesion = leer_json(ruta)
    existe = None
    for c in leer_sesion:
        if int(c["dni"]):
            existe = c
            leer_sesion.remove(existe)
            guardar_json("data/sesion_actual.json",leer_sesion)
            return
        else:
            print("No hay ninguna sesion abierta.")
        
        
def restablecer_pin(ruta):
    '''
    Si se olvido el PIN, puede restablecerlo. Ingresa el dni de la cuenta que desea cambiar
    '''
    dni = int(input("Ingrese el numero de DNI: "))
    dni_encontrado,indice = buscar_dni(dni,ruta)
    leer_cuentas = leer_json(ruta)
    pin = int(input("Ingrese su nuevo PIN: "))
    pin_reingresar = int(input("Reingrese su nuevo PIN: "))
    
    if pin_reingresar == pin:
        confirmar_pin = input("Desea confirmar su nuevo PIN (si/no): ").lower()
        if confirmar_pin == "si":
            leer_cuentas[indice]["pin"] = pin_reingresar
            guardar_json(ruta, leer_cuentas)
            print("El PIN ha sido cambiado correctamente.")
    else:
        print("Ha ingresado mal el PIN. Vuelva a intentarlo.")
        return restablecer_pin()