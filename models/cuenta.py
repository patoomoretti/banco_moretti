class Cuenta:
    
    def __init__(self, numero,dni,tipo_cuenta,saldo):
        self.numero = numero
        self.dni = dni
        self.tipo_cuenta = tipo_cuenta
        self.saldo = saldo
        
        
    def __str__(self):
        return f"Cuenta N°{self.numero} de tipo {self.tipo_cuenta} dispone de un saldo de {self.saldo} (DNI: {self.dni})"
