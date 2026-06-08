from database import db

class Movimiento(db.Model):
    __tablename__ = "movimientos"

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer, db.ForeignKey("clientes.dni"), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    detalle = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.String(50), nullable=False)
    monto = db.Column(db.Float, nullable=False)

    cliente = db.relationship("Cliente", backref="movimientos")

    def __str__(self):
        return f"{self.tipo} | ${self.monto} | {self.fecha}"