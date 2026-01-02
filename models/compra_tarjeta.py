class CompraTarjeta: 
    
    def __init__(self, dni, producto,importe,cuotas,importe_cuotas):
        self.dni = dni
        self.producto = producto
        self.importe = importe
        self.cuotas = cuotas
        self.importe_cuotas = importe_cuotas
        
    def __str__(self):
        return f"Producto: {self.producto} | Importe: ${self.importe}| Cuotas: {self.cuotas} | Importe Cuotas: ${self.importe_cuotas}"
