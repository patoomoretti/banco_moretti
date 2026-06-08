from models.cliente import Cliente
from models.transferencia import Transferencia
from models.compra_tarjeta import CompraTarjeta
from datetime import datetime
from utils.helpers import * 

class ClienteService: 
    
    def consultar_saldo(self):
        '''
        Consulta el saldo que tiene actualmente
        '''
        dni = int(input("Ingrese el DNI: "))
        cuenta,indice = buscar_dni(dni,"data/cuentas_bancarias.json")
        leer_cuenta = leer_json("data/cuentas_bancarias.json")
        
        print("-----------------------")
        print(f"El saldo es de ${leer_cuenta[indice]['saldo']}")
        print("-----------------------")
 

    def depositar_dinero(self):
        '''
        Desposita el importe seleccionado a una cuenta
        '''
        dni = int(input("Ingrese el DNI de la cuenta a depositar: "))
        cuenta,indice = buscar_dni(dni,"data/cuentas_bancarias.json")
        leer_cuenta = leer_json("data/cuentas_bancarias.json")
        ingreso_dinero = int(input("Ingrese la cantidad de dinero que desea depositar: "))
        
        leer_cuenta[indice]["saldo"] += ingreso_dinero
        guardar_json("data/cuentas_bancarias.json",leer_cuenta)
        print("-----------------------")
        print(f"El nuevo saldo es de ${leer_cuenta[indice]['saldo']}")
        print("-----------------------")

        
    def retirar_dinero(self):
        '''
        Retira el efectivo deseado ingresando el dni
        '''
        leer_cuenta = leer_json("data/cuentas_bancarias.json")
        dni = int(input("Ingrese el DNI: "))
        cuenta,indice = buscar_dni(dni,"data/cuentas_bancarias.json")
        
        retiro_dinero = int(input("Ingrese la cantidad que desea retirar: "))
        
        leer_cuenta[indice]["saldo"] -= retiro_dinero
        if leer_cuenta[indice]["saldo"] < 0:
            print("-----------------------")
            print("Fondos insuficientes.")
            print("-----------------------")
            return
        else:
            print("Operacion exitosa")
            guardar_json("data/cuentas_bancarias.json",leer_cuenta)
            print("-----------------------")
            print(f"Su nuevo saldo es ${leer_cuenta[indice]['saldo']}")
            print("-----------------------")
            
              
    def transferir_dinero(self):
        '''
        Transferencia de dinero de una cuenta a otra verificando si existen las cuentas y que tenga saldo para poder hacerlo. Tambien se guarda cada transferencia realizada.
        '''
        leer_cuenta = leer_json("data/cuentas_bancarias.json")
        dni_origen = int(input("Ingrese el DNI de la cuenta origen: "))
        dni_destino = int(input("Ingrese el DNI a la cuenta destino: "))
        fecha = datetime.now().strftime("%d-%m-%y  %H:%M")
        
        # Validamos que el dni origen y el dni destino no sean iguales
        if dni_origen == dni_destino:
            print("-----------------------")
            print("No se puede transferir a una misma cuenta.")
            print("-----------------------")
            return 
        
        cuenta_origen,indice = buscar_dni(dni_origen,"data/cuentas_bancarias.json")
        cuenta_destino,indice = buscar_dni(dni_destino,"data/cuentas_bancarias.json")
        
        # Validamos de que las cuentas existan
        if dni_origen != cuenta_origen["dni"] or dni_destino != cuenta_destino["dni"]:
            print("-----------------------")
            print("El DNI no tiene una cuenta en el Banco.")
            print("-----------------------")
            return
        
        for i, c in enumerate(leer_cuenta):
            if c["dni"] == dni_origen:
                indice_origen = i
                origen = c
            if c["dni"] == dni_destino:
                indice_destino = i
                destino = c
                
        monto = int(input("Ingrese el monto que desea transferir: "))
        # Validamos que el monto no sea cero o negativo
        if monto > origen["saldo"]:
            print("----------------------")
            print("No cuenta con los fondos suficientes para hacer la transferencia.")
            print("----------------------")
            return
        
        
        leer_transferencia = leer_json("data/transferencias.json")
        nueva_transferencia = Transferencia(dni_origen,dni_destino,monto,fecha)
        transferencia_dict = {
            "dni_origen": dni_origen,
            "dni_destino": nueva_transferencia.destino,
            "monto": nueva_transferencia.monto,
            "fecha": nueva_transferencia.fecha
        }
        
        if int(origen["saldo"]) > 0:
            leer_cuenta[indice_origen]["saldo"] -= monto
            leer_cuenta[indice_destino]["saldo"] += monto
            leer_transferencia.append(transferencia_dict)
            print("----------------------")
            print(f"Se ha realizado la transferencia de ${monto}")
            print("----------------------")
            guardar_json("data/cuentas_bancarias.json", leer_cuenta)
            guardar_json("data/transferencias.json", leer_transferencia)
        else:
            print("No ha sido posible transferir ya que no cuenta con los fondos necesarios.")
            return
        
        
    def agregar_consumo_tarjeta(self):
        '''
        Simulamos consumos como para que despues al pagar la tarjeta se lo cobremos. Se puede pagar en cuotas y tener intereses.
        '''
        dni = int(input("Ingrese el DNI: "))
        cuenta,indice = buscar_dni(dni,"data/cuentas_bancarias.json")
        leer_cuenta = leer_json("data/cuentas_bancarias.json")
        leer_consumos = leer_json("data/consumos_tarjeta_credito.json")

        if not leer_cuenta[indice]["tarjeta_credito"]:
            print("No tiene tarjeta de credito.")
            return
        
        producto = input("Tipo de producto (Heladera/Pantalon/Pintura/etc):")
        importe = int(input("Importe: "))
        while importe <= 0:
            print("El importe tiene que ser mayor que el numero cero. Reingrese el importe")
            importe = int(input("Importe: "))
            
        cuotas = int(input("Cuotas (0/3/6/9): "))
        while cuotas != 0 and cuotas != 3 and cuotas != 6 and cuotas != 9:
            print("Numero incorrecto. Reingrese el numero de cuotas.")
            cuotas = int(input("Cuotas (0/3/6/9): "))
            
        # Intereses por hacerlo en cuotas
        if cuotas == 3:
            intereses = importe * 10/100
            importe += intereses
            importe_cuotas = importe / cuotas
            print(f"3 cuotas con 10% de interes")
        elif cuotas == 6:
            intereses = importe * 20/100
            importe += intereses
            importe_cuotas = importe / cuotas
            print(f"6 cuotas con 20% de interes")
        elif cuotas == 9: 
            intereses = importe * 30/100
            importe += intereses
            importe_cuotas = importe / cuotas
            print(f"9 cuotas con 30% de interes")
        else:
            importe_cuotas = importe
            
        nueva_compra = CompraTarjeta(dni,producto,importe,cuotas,importe_cuotas)
        
        agregar_producto = {
            "producto": nueva_compra.producto,
            "importe": nueva_compra.importe, 
            "cuotas": nueva_compra.cuotas,
            "importe_cuotas": nueva_compra.importe_cuotas
        }
        
        # Buscar si el DNI ya tiene compras guardadas
        encontrado = False
        for cliente in leer_consumos:
            if cliente["dni"] == dni:
                cliente["compra"].append(agregar_producto)
                encontrado = True
                break

        # Si no existe el dni, crear uno nuevo
        if not encontrado:
            leer_consumos.append({
                "dni": dni,
                "compra": [agregar_producto]
            })
        
        guardar_json("data/consumos_tarjeta_credito.json",leer_consumos)
        
        for c in leer_consumos:
            leer_cuenta[indice]["tarjeta_credito"]["consumos"] += importe
            guardar_json("data/cuentas_bancarias.json",leer_cuenta)

    
        
    def consultar_gastos_tarjeta(self):
        '''
        Consultamos los gastos que hizo el cliente
        '''
        dni = int(input("Ingrese el DNI (consultar gastos tarjeta): "))
        cuenta,indice = buscar_dni(dni,"data/cuentas_bancarias.json")
        leer_cuenta = leer_json("data/cuentas_bancarias.json")
        
        print("----------------------")
        print(f"Consumos: ${leer_cuenta[indice]['tarjeta_credito']['consumos']}")
        print("----------------------")
        
        
    def pagar_tarjeta(self):
        '''
        Paga un monto elegido. Es con plata en cuenta con la que disponga
        '''
        dni = int(input("Ingrese el DNI de la cuenta que desea pagar: "))
        cuenta,indice = buscar_dni(dni,"data/cuentas_bancarias.json")
        leer_cuenta = leer_json("data/cuentas_bancarias.json")
        
        if leer_cuenta[indice]["tarjeta_credito"] == False:
            print("-----------------------")
            print("No posee Tarjeta de Credito")
            print("-----------------------")
            return
        if leer_cuenta[indice]["tarjeta_credito"]["consumos"] <= 0:
            print("-----------------------")
            print("No tiene consumos hechos.")
            print("-----------------------")
            return
        
        print("----------------------")
        print(f"Saldo: ${leer_cuenta[indice]["saldo"]}")
        print(f"Total de consumos: ${leer_cuenta[indice]['tarjeta_credito']['consumos']}")
        print("----------------------")
        tipo_pago = input("Tipo de pago (parcial/total): ").lower()
        monto_pagar = int(input("Ingrese el monto que desea pagar: "))
        
        if tipo_pago == "total":
            if leer_cuenta[indice]["saldo"] < leer_cuenta[indice]["tarjeta_credito"]["consumos"]:
                print("----------------------")
                print(f"No dispone de saldo suficiente para hacer el pago total de la tarjeta.")
                return
            else:
                leer_cuenta[indice]["tarjeta_credito"]["consumos"] -= monto_pagar
                leer_cuenta[indice]["saldo"] -= monto_pagar
                if leer_cuenta[indice]["tarjeta_credito"]["consumos"] < 0:
                    print("---- No se puede hacer pagos por mas valor. Reintente nuevamente ----")
                    return
                print("----------------------")
                print(f"Saldo actualizado: ${leer_cuenta[indice]['saldo']}")
                print(f"Consumos: ${leer_cuenta[indice]['tarjeta_credito']['consumos']}")
                print("----------------------")
                guardar_json("data/cuentas_bancarias.json", leer_cuenta)
        else:
            leer_cuenta[indice]["tarjeta_credito"]["consumos"] -= monto_pagar
            leer_cuenta[indice]["saldo"] -= monto_pagar
            print("----------------------")
            print(f"Saldo actualizado: ${leer_cuenta[indice]['saldo']}")
            print(f"Consumos: ${leer_cuenta[indice]["tarjeta_credito"]["consumos"]}")
            print("----------------------")
            guardar_json("data/cuentas_bancarias.json", leer_cuenta)
            print(f"Total que se debe: ${leer_cuenta[indice]["tarjeta_credito"]["consumos"]}")
                

    def resumen_tarjeta(self):
        '''
        Consulta los consumos que hizo en el mes
        '''
        dni = int(input("Ingrese el DNI: "))
        cuenta,indice = buscar_dni(dni,"data/consumos_tarjeta_credito.json")
        leer_consumos = leer_json("data/consumos_tarjeta_credito.json")
        
        print("----- Resumen Tarjeta Credito -----")
        if int(leer_consumos[indice]["dni"]) == dni:
            for compra in leer_consumos[indice]['compra']:
                print(f"Producto: {compra['producto']} | "f"Importe: ${compra['importe']} | " f"Cuotas: {compra['cuotas']} | "f"Importe Cuota: ${compra['importe_cuotas']:.2f}")


        
        
        
        