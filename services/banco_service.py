from models.cliente import Cliente
from models.cuenta import Cuenta
from models.tarjetas import *
from utils.helpers import *
import random


class BancoService:

    def __init__(self):
        self.clientes = {}
        self.cuentas = {}

    def agregar_cliente(self):
        '''
        Crea el cliente en el banco.
        '''
        nombre = input("Ingrese el nombre: ").capitalize()
        apellido = input("Ingrese el apellido: ").capitalize()
        dni = int(input("Ingrese el DNI: "))

        chequear_datos = input(f"Confirma que los datos son correctos? {nombre}{apellido} | DNI: {dni} (si/no): ")

        while chequear_datos == "no":
            print("Por favor, ingrese los datos nuevamente.")
            nombre = input("Ingrese el nombre: ").capitalize()
            apellido = input("Ingrese el apellido: ").capitalize()
            dni = int(input("Ingrese el DNI: "))
            chequear_datos = input(
                f"Confirma que los datos son correctos? {nombre} {apellido} {dni} (si/no): ")

        nuevo_cliente = Cliente(nombre, apellido, dni)
        cliente_dict = {
            "nombre": nuevo_cliente.nombre,
            "apellido": nuevo_cliente.apellido,
            "dni": nuevo_cliente.dni
        }

        leer_cliente = leer_json("data/clientes.json")

        # Agregarlo a la lista
        cliente_existe = False
        for c in leer_cliente:
            if c["dni"] == dni:
                cliente_existe = True
                break

        if cliente_existe:
            print("El cliente ya esta registrado.")
        else:
            leer_cliente.append(cliente_dict)
            print(f"El cliente {nuevo_cliente.nombre} {nuevo_cliente.apellido} ha sido registrado correctamente.")

        guardar_json("data/clientes.json",leer_cliente)


    def crear_cuenta(self):
        '''
        Crea cuenta bancaria para el cliente que ya se encuentre registrado en el banco
        '''
        id_cuenta = f"{random.randint(0, 999999):06d}"
        dni = int(input("Ingrese el DNI del cliente para crear la cuenta: "))
        cuentas,indice = buscar_dni(dni,"data/clientes.json")
        leer_cuentas = leer_json("data/cuentas_bancarias.json")
        
        for c in leer_cuentas:
            if int(c["dni"]) == dni:
                print("--------------------------")
                print("El cliente ya tiene una cuenta registrada.")
                print("--------------------------")
                return

        numero = id_cuenta
        tipo_cuenta = input("Ingrese el tipo de cuenta (Ahorro/ Corriente): ").capitalize()
        saldo = 0

        nueva_cuenta = Cuenta(numero, dni, tipo_cuenta, saldo)

        cuenta_dict = {
            "numero": nueva_cuenta.numero,
            "dni": nueva_cuenta.dni,
            "tipo_cuenta": nueva_cuenta.tipo_cuenta,
            "saldo": 0,
            "tarjeta_credito": False,
            "tarjeta_debito": False
        }

        leer_cuentas.append(cuenta_dict)
        print("--------------------------")
        print(f"Cuenta N°{nueva_cuenta.numero} ({nueva_cuenta.tipo_cuenta}) creada correctamente para DNI {dni}")
        print("--------------------------")
        
        guardar_json("data/cuentas_bancarias.json", leer_cuentas)


    def buscar_cliente(self):
        ''''
        Buscar el cliente por el numero de DNI
        '''
        dni = int(input("Ingrese el DNI del cliente que desea buscar: "))
        clientes,indice = buscar_dni(dni,"data/clientes.json")
        leer_clientes = leer_json("data/clientes.json")
        
        if int(clientes["dni"]) == dni:
            print("--------------------------")
            print(f"El cliente ha sido encontrado.")
            print(f"Nombre y Apellido: {clientes['nombre']} {clientes['apellido']}")
            print(f"DNI: {dni}")
            print("--------------------------")
            

    def agregar_producto(self):
        '''
        Agregar un producto (tarjeta debito o credito) y verificar si ya tiene el producto agregado
        '''
        leer_cuentas = leer_json("data/cuentas_bancarias.json")
        dni = int(input("Ingrese el DNI del cliente al que desea agregar un producto: "))
        cliente,indice = buscar_dni(dni,"data/cuentas_bancarias.json")
        
        if int(cliente["dni"]) != dni:
            print("El cliente no existe.")
            return

        numero = f"{random.randint(0000, 9999):04d} - {random.randint(0000, 9999):04d} - {random.randint(0000, 9999):04d} - {random.randint(0000, 9999):04d}"
        fecha_vencimiento = f"{random.randint(1, 12):02d} - {random.randint(27, 36):02d}"
        cvv = f"{random.randint(000, 999):03d}"
        consumos = 0

        nueva_tarjeta_credito = Tarjeta_Credito(numero, fecha_vencimiento, cvv, consumos)

        tarjeta_dict = {
            "numero": nueva_tarjeta_credito.numero,
            "fecha_vencimiento": nueva_tarjeta_credito.fecha_vencimiento,
            "cvv": nueva_tarjeta_credito.cvv,
            "consumos": consumos
        }

        producto = input("Elija que producto decide agregar (Debito/Credito): ").capitalize()
        while producto != "Debito" and producto != "Credito":
            print("Opcion invalida. Intente nuevamente.")
            producto = input("Elija que producto decide agregar (Debito/Credito): ").capitalize()

        if producto == "Debito":
            leer_cuentas[indice]["tarjeta_debito"] = tarjeta_dict
            guardar_json("data/cuentas_bancarias.json", leer_cuentas)
            print("--------------------------")
            print("Tarjeta de Debito agregada correctamente")
            print("--------------------------")
        elif producto == "Credito":
            leer_cuentas[indice]["tarjeta_credito"] = tarjeta_dict
            guardar_json("data/cuentas_bancarias.json", leer_cuentas)
            print("--------------------------")
            print("Tarjeta de Credito agregada correctamente")
            print("--------------------------")



    def eliminar_producto(self):
        '''
        Buscamos el DNI y le damos de baja un producto seleccionado
        '''
        dni = int(input("Ingrese el numero de DNI: "))
        resultado,indice= buscar_dni(dni, "data/cuentas_bancarias.json")
        print(f"DNI {resultado['dni']} encontrado")
        leer_cuenta= leer_json("data/cuentas_bancarias.json")

        producto = input("Que producto desea dar de baja (Credito/Debito): ").capitalize()

        if producto == "Credito":
            leer_cuenta[indice]["tarjeta_credito"] = False
            guardar_json("data/cuentas_bancarias.json", leer_cuenta)
            print("---------------------")
            print("La tarjeta de credito ha sido eliminada correctamente.")
            print("---------------------")
        else:
            leer_cuenta[indice]["tarjeta_debito"] = False
            guardar_json("data/cuentas_bancarias.json", leer_cuenta)
            print("---------------------")
            print("La tarjeta de debito ha sido eliminada correctamente.")
            print("---------------------")


    def solicitar_datos_cliente(self):
        '''
        Pido toda la informacion sobre un cliente (dni,nombre,apellido,cuenta,tarjetas,etc)
        '''
        dni = int(input("Ingrese el DNI del cliente: "))
        cuentas, indice = buscar_dni(dni, "data/cuentas_bancarias.json")
        clientes, indice = buscar_dni(dni, "data/clientes.json")

        print("-------------------------")
        print(" ------ Cliente ------")
        print(f"Nombre: {clientes['nombre']}")
        print(f"Apellido: {clientes['apellido']}")
        print(f"DNI: {clientes['dni']}")
        print(" ------ Datos Cuenta ------")
        print(f"Numero Cuenta: {cuentas['numero']}")
        print(f"Tipo de Cuenta: {cuentas['tipo_cuenta']}")
        print(f"Saldo: {cuentas['saldo']}")
        if cuentas["tarjeta_credito"]:
            print(f"Tarjeta de Credito: Tiene")
        else:
            print(f"Tarjeta de Credito: No tiene")

        if cuentas["tarjeta_debito"]:
            print(f"Tarjeta de Debito: Tiene")
        else:
            print(f"Tarjeta de Debito: No tiene")
        print("-------------------------")


    def mostrar_transferencia_cliente(self):
        '''
        Se ingresa el dni y se muestran todas las transferencias que realizo. Mostrando el dni destino,importe y la fecha
        '''
        dni = int(input("Ingrese el DNI: "))
        leer_transferencia = leer_json("data/transferencias.json")

        print(f"----- Transferecias Realizadas del DNI N* {dni} -----")
        encontradas = False
        for t in leer_transferencia:
            if t["dni_origen"] == dni:
                print(f"DNI Destino: {t['dni_destino']}")
                print(f"Monto: ${t['monto']}")
                print(f"Fecha: {t['fecha']}")
                print("------------------------")
                encontradas = True

        if not encontradas:
            print("No hay ninguna transferencia realizada.")
