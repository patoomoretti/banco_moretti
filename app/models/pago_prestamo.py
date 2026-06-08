from database import db

class PagoPrestamo(db.Model):
    __tablename__ = "pagos_prestamo"

    id = db.Column(db.Integer, primary_key=True)
    prestamo_id = db.Column(db.Integer, db.ForeignKey("prestamos.id"), nullable=False)
    cuota_nro = db.Column(db.Integer, nullable=False)
    monto = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.String(50), nullable=False)

    prestamo = db.relationship("Prestamo", backref="pagos")

    def __str__(self):
        return f"Cuota {self.cuota_nro} | ${self.monto} | {self.fecha}"