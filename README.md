# 🏦 Banco Moretti

Proyecto personal de práctica. La idea es simular el funcionamiento de una entidad bancaria real, con sus operaciones típicas y dos perfiles de usuario diferenciados — cliente y empleado — cada uno con su propio panel y conjunto de operaciones. Desarrollado con Flask y SQLAlchemy.

---

## 🛠️ Tecnologías

- Python 3.12
- Flask
- SQLAlchemy + Flask-Migrate (Alembic)
- Jinja2
- SCSS → compilado a `static/css/main.css`
- python-dotenv

---

## 📁 Estructura

```
app/
├── app.py                  # Entry point y configuración Flask
├── database.py             # Instancia de SQLAlchemy
├── models/                 # Modelos ORM
├── routes/                 # Blueprints (auth, cliente, empleado)
├── services/               # Lógica de negocio
├── utils/helpers.py        # Funciones auxiliares (auth, formateo)
├── templates/              # HTML con Jinja2
├── static/                 # CSS, SCSS, JS
├── data/                   # JSONs de datos de prueba
└── migrations/             # Alembic
```

---

## ⚙️ Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Crear archivo `.env`

```env
SECRET_KEY=tu_clave_secreta
DATABASE_URL=sqlite:///banco.db
```

### 3. Aplicar migraciones

```bash
flask db upgrade
```

### 4. Correr la app

```bash
python app.py
```

Disponible en `http://localhost:5000`.


### 5. Crear usuario empleado

Una vez levantada la app, entrá a `/registrar_empleado` para crear el usuario empleado con el DNI y PIN que quieras.

---

## 👤 Roles

| Rol      | URL de acceso |
|----------|---------------|
| Cliente  | `/login`      |
| Empleado | `/admin`      |

La sesión se maneja con `flask.session` usando DNI y rol.

---

## 🗄️ Base de datos

| Tabla             | Descripción |
|-------------------|-------------|
| `usuarios`        | Credenciales (DNI + PIN) y rol |
| `clientes`        | Datos personales |
| `empleados`       | Datos del personal |
| `cuentas`         | Saldo en pesos y dólares |
| `tarjetas`        | Visa/Master, débito/crédito, límite y consumos |
| `prestamos`       | Monto, cuotas, tasa de interés y estado |
| `movimientos`     | Historial de operaciones |
| `transferencias`  | Transferencias entre clientes |
| `compras_tarjeta` | Consumos con tarjeta de crédito en cuotas |
| `pagos_prestamo`  | Pagos de cuotas |

---

## ✅ Funcionalidades

### Cliente
- Registro, login y restablecimiento de PIN
- Ver saldo en pesos y dólares
- Depositar y retirar dinero
- Transferir dinero a otro cliente por DNI
- Ver historial de movimientos y transferencias
- Solicitar préstamo (monto, plazo, destino)
- Tarjetas Visa/Master débito y crédito: ver disponible y límite
- Agregar consumo con tarjeta de crédito (con cuotas)
- Pagar tarjeta (total o parcial)
- Resumen de tarjeta por período

### Empleado
- Dashboard con métricas del día (depósitos, transferencias, últimos clientes)
- Alta y baja de clientes
- Buscar cliente por DNI y ver/editar su perfil
- Alta de cuenta bancaria para un cliente
- Alta y baja de productos (tarjetas)
- Solicitar préstamo para un cliente