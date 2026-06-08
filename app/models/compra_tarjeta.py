from database import db

class CompraTarjeta(db.Model):
    __tablename__ = "compras_tarjeta"

    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer, db.ForeignKey("clientes.dni"), nullable=False)
    tarjeta_id = db.Column(db.Integer, db.ForeignKey("tarjetas.id"), nullable=False)
    producto = db.Column(db.String(200), nullable=False)
    importe = db.Column(db.Float, nullable=False)
    importe_cuota = db.Column(db.Float, nullable=False)
    cuotas_totales = db.Column(db.Integer, nullable=False)
    cuota_actual = db.Column(db.Integer, nullable=False, default=1)
    fecha = db.Column(db.String(50), nullable=False)
    periodo = db.Column(db.String(10), nullable=False)

    cliente = db.relationship("Cliente", backref="compras")
    tarjeta = db.relationship("Tarjeta", backref="compras")

    def __str__(self):
        return f"{self.producto} | ${self.importe} | Cuota {self.cuota_actual}/{self.cuotas_totales}"