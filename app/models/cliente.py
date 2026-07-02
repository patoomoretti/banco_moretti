from database import db

class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer, unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    piso = db.Column(db.Integer, nullable=True)
    departamento = db.Column(db.String(10), nullable=True)
    telefono = db.Column(db.BigInteger, nullable=False)
    email = db.Column(db.String(150), nullable=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido} (DNI: {self.dni})"