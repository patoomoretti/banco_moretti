from database import db

class Transferencia(db.Model):
    __tablename__ = "transferencias"

    id = db.Column(db.Integer, primary_key=True)
    dni_origen = db.Column(db.Integer, db.ForeignKey("clientes.dni"), nullable=False)
    dni_destino = db.Column(db.Integer, db.ForeignKey("clientes.dni"), nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.String(50), nullable=False)

    origen = db.relationship("Cliente", foreign_keys=[dni_origen], backref="transferencias_enviadas")
    destino = db.relationship("Cliente", foreign_keys=[dni_destino], backref="transferencias_recibidas")

    def __str__(self):
        return f"De {self.dni_origen} a {self.dni_destino} | ${self.monto} | {self.fecha}"