from database import db

class Usuario(db.Model):
    __tablename__ = "usuarios"
    
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer, unique=True, nullable=False)
    pin = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(20), nullable=False, default="cliente")

    def __str__(self):
        return f"Usuario: {self.dni}"