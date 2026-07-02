from datetime import datetime
from app import db

class ExtraccionDeposito(db.Model):
    __tablename__ = "extraccion_deposito"
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    detalle = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    monto = db.Column(db.Float, nullable=False)

    def __str__(self):
        return f"Tipo: {self.tipo} | Detalle: {self.detalle} | Fecha: {self.fecha} | Monto: {self.monto}"
        