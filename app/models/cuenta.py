from database import db

class Cuenta(db.Model):
    __tablename__ = "cuentas"

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, unique=True, nullable=False)
    dni = db.Column(db.Integer, db.ForeignKey("clientes.dni"), nullable=False)
    tipo_cuenta = db.Column(db.String(50), nullable=False)
    saldo = db.Column(db.Float, nullable=False, default=0.0)
    saldo_dolar = db.Column(db.Float, nullable=True, default=0.0)

    cliente = db.relationship("Cliente", backref="cuentas")

    def __str__(self):
        return f"Cuenta N°{self.numero} | Tipo: {self.tipo_cuenta} | Saldo: {self.saldo}"