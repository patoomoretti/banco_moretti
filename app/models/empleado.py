from database import db

class Empleado(db.Model):
    __tablename__ = "empleados"

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer, unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"