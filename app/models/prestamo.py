from database import db

class Prestamo(db.Model):
    __tablename__ = "prestamos"

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer, db.ForeignKey("clientes.dni"), nullable=False)
    monto_solicitado = db.Column(db.Float, nullable=False)
    monto_cuota = db.Column(db.Float, nullable=False)
    cuotas_totales = db.Column(db.Integer, nullable=False)
    cuotas_pagas = db.Column(db.Integer, nullable=False, default=0)
    tasa_interes = db.Column(db.Float, nullable=False)
    motivo = db.Column(db.String(200), nullable=False)
    fecha_solicitud = db.Column(db.String(50), nullable=False)
    total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default="activo")
    fecha_fin = db.Column(db.String(50), nullable=True)

    cliente = db.relationship("Cliente", backref="prestamos")

    def __str__(self):
        return f"Préstamo de ${self.monto_solicitado} | Cuotas: {self.cuotas_totales} | Estado: {self.estado}"