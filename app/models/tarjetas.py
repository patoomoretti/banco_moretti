from database import db

class Tarjeta(db.Model):
    __tablename__ = "tarjetas"

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(30), unique=True, nullable=False)
    dni = db.Column(db.Integer, db.ForeignKey("clientes.dni"), nullable=False)
    marca = db.Column(db.String(20), nullable=False)  # visa / master
    tipo = db.Column(db.String(20), nullable=False)   # credito / debito
    fecha_vencimiento = db.Column(db.String(10), nullable=False)
    cvv = db.Column(db.Integer, nullable=False)
    consumos = db.Column(db.Float, nullable=False, default=0.0)
    limite = db.Column(db.Float, nullable=False, default=5000000)

    cliente = db.relationship("Cliente", backref="tarjetas")

    def __str__(self):
        return f"Tarjeta {self.marca} {self.tipo} N° {self.numero}"