from services.banco_service import BancoService
from services.cliente_service import ClienteService
from utils.helpers import *


def main():
    banco = BancoService()
    cliente = ClienteService()

    print("\n=== BIENVENIDO AL BANCO MORETTI ===")
    opcion_menu = input("Seleccione una opción (Banco / Cliente): ").capitalize()

    if opcion_menu == "Cliente":
        while True:
            print("1. Registrarme")
            print("2. Iniciar Sesion")
            print("3. Reestablecer PIN")
            print("0. Salir")
            opcion_ingreso = input("Seleccione una opción: ")
            
            if opcion_ingreso == "1":
                registrar_cuenta("data/usuario_cliente.json")
            elif opcion_ingreso == "2":
                loguear_cuenta("data/usuario_cliente.json")
                while True:
                    print("\n=== MENÚ CLIENTE ===")
                    print("1. Consultar Saldo")
                    print("2. Depositar Dinero")
                    print("3. Retirar Dinero")
                    print("4. Transferir")
                    print("5. Compra tarjeta credito")
                    print("6. Consultar gastos tarjeta")
                    print("7. Pagar tarjeta credito")
                    print("8. Resumen tarjeta credito")
                    print("0. Cerrar Sesion")
                    opcion = input("Seleccione una opción: ")

                    if opcion == "1":
                        cliente.consultar_saldo()
                    elif opcion == "2":
                        cliente.depositar_dinero()
                    elif opcion == "3":
                        cliente.retirar_dinero()
                    elif opcion == "4":
                        cliente.transferir_dinero()
                    elif opcion == "5":
                        cliente.agregar_consumo_tarjeta()
                    elif opcion == "6":
                        cliente.consultar_gastos_tarjeta()
                    elif opcion == "7":
                        cliente.pagar_tarjeta()
                    elif opcion == "8":
                        cliente.resumen_tarjeta()
                    elif opcion == "0":
                        cerrar_sesion("data/sesion_actual.json")
                        print("Sesion cerrada.")
                        break
                    else:
                        print("Opción inválida. Intente nuevamente.")
            elif opcion_ingreso == "3":
                restablecer_pin()
            elif opcion_ingreso == "0":
                print("Saliendo del sistema...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
    elif opcion_menu == "Banco":
        # while True:
        #     print("1. Registrarme")
        #     print("2. Iniciar Sesion")
        #     print("3. Restablecer PIN")
        #     print("0. Salir")
        #     opcion_ingreso = input("Seleccione una opción: ")

        #     if opcion_ingreso == "1":
        #         registrar_cuenta("data/usuario_empleado.json")
        #     elif opcion_ingreso == "2":
        #         loguear_cuenta("data/usuario_empleado.json")
                while True:
                    print("\n=== MENÚ BANCO ===")
                    print("1. Agregar cliente")
                    print("2. Crear cuenta")
                    print("3. Buscar cuenta")
                    print("4. Agregar tarjeta a cuenta")
                    print("5. Eliminar tarjeta de cuenta")
                    print("6. Mostrar datos cliente")
                    print("7. Mostrar transferencia cliente")
                    print("0. Salir")
                    opcion = input("Seleccione una opción: ")

                    if opcion == "1":
                        banco.agregar_cliente()
                    elif opcion == "2":
                        banco.crear_cuenta()
                    elif opcion == "3":
                        banco.buscar_cliente()
                    elif opcion == "4":
                        banco.agregar_producto()
                    elif opcion == "5":
                        banco.eliminar_producto()
                    elif opcion == "6":
                        banco.solicitar_datos_cliente()
                    elif opcion == "7":
                        banco.mostrar_transferencia_cliente()
                    elif opcion == "0":
                        print("Saliendo del sistema...")
                        break
                    else:
                        print("Opción inválida. Intente nuevamente.")
            # elif opcion_ingreso == "3":
            #     restablecer_pin()
            # elif opcion_ingreso == "0":
            #     print("Saliendo del sistema...")
            #     break
            # else:
            #     print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
