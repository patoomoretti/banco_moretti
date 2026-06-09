from flask import Flask, render_template, request, redirect,session
from utils.helpers import *
from routes.cliente_route import cliente_bp
from routes.empleado_route import empleado_bp
from routes.auth_route import auth_bp
from dotenv import load_dotenv
# Base de datos
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# --------
from database import db
from models.usuarios import Usuario
from models.cliente import Cliente
from models.cuenta import Cuenta
from models.tarjetas import Tarjeta
import os


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


# Registrar blueprints
app.register_blueprint(cliente_bp)
app.register_blueprint(empleado_bp)
app.register_blueprint(auth_bp)

# === Rutas del sitio ===
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/sobre_nosotros")
def sobre_nosotros():
    return render_template("sobre_nosotros.html")


if __name__ == "__main__":
    app.run(debug=True)