class ExtraccionDeposito: 
    
    def __init__(self, tipo, detalle, fecha, monto):
        self.tipo = tipo
        self.detalle = detalle
        self.fecha = fecha
        self.monto = monto
    
    def __str__(self):
        return f"Tipo: {self.tipo} | Detalle: {self.detalle} | Fecha: {self.fecha} | Monto: {self.monto}"
        