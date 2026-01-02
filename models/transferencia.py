class Transferencia:
    
    def __init__(self,dni_origen,dni_destino,monto,fecha):
        self.origen = dni_origen
        self.destino = dni_destino
        self.monto = monto
        self.fecha = fecha
        
    def __str__(self):
        return f"DNI Origen: {self.origen} | DNI Destino: {self.destino} | Monto: ${self.monto}) | Fecha: {self.fecha}"