class Empleado:
    def __init__(self,nombre,apellido,dni,sector):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.sector = sector
        
    def __str__(self):
        return f"{self.nombre} {self.apellido}"