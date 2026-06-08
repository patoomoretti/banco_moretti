class Usuario:
    def __init__(self, dni, pin):
        self.dni = dni
        self.pin = pin
        
    def __str__(self):
        return f"Usuario: {self.dni})"
    
