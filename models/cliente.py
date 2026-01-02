class Cliente:
    def __init__(self,nombre,apellido, dni):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        
    def __str__(self):
        return f"{self.nombre} {self.apellido} (DNI: {self.dni})"
    
