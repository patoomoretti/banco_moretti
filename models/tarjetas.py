class Tarjeta_Credito:
    def __init__(self,numero,fecha_vencimiento,cvv,consumos):
        self.numero = numero
        self.fecha_vencimiento = fecha_vencimiento,
        self.cvv = cvv,
        self.consumos = consumos
        
    def __str__(self):
        return f"Tarjeta de Credito N° {self.numero} con fecha de vencimiento {self.fecha_vencimiento}"
    
    
    
class Tarjeta_Debito:
    def __init__(self,numero,fecha_vencimiento,cvv):
        self.numero = numero
        self.fecha_vencimiento = fecha_vencimiento,
        self.cvv = cvv
        
    def __str__(self):
        return f"Tarjeta de Debito N° {self.numero} con fecha de vencimiento {self.fecha_vencimiento}"
        