# Configuración SQLite con Flask SQLAlchemy - Guía Completa

## 📋 Tabla de Contenidos

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Inicialización](#inicialización)
- [Uso Práctico](#uso-práctico)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes)
- SQLite (incluido en Python)

## 📦 Instalación

### 1. Crear entorno virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Verificar instalación

```bash
python -c "import flask; import flask_sqlalchemy; print('✓ Instalación correcta')"
```

---

## ⚙️ Configuración

### Estructura de Configuración

El proyecto usa **3 configuraciones diferentes** según el entorno:

#### `app/config.py` - Configuraciones por Entorno

```python
# DESARROLLO - SQLite en archivo
DevelopmentConfig:
  DATABASE_URL: sqlite:///instance/billing_system.db
  SQLALCHEMY_ECHO: True
  DEBUG: True

# TESTING - SQLite en memoria
TestingConfig:
  DATABASE_URL: sqlite:///:memory:
  SQLALCHEMY_ECHO: False
  DEBUG: True

# PRODUCCIÓN - SQLite optimizado
ProductionConfig:
  DATABASE_URL: sqlite:///data/billing_system_prod.db
  DEBUG: False
```

### Variables de Entorno (`.env`)

```env
# Configuración Flask
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production

# Base de Datos
DATABASE_URL=sqlite:///instance/billing_system.db

# Servidor
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000
```

### Parámetros SQLite Importantes

```python
# En app/config.py
SQLALCHEMY_ENGINE_OPTIONS = {
    'connect_args': {
        'timeout': 15,                # Espera max de bloqueo (segundos)
        'check_same_thread': False    # Múltiples threads
    },
    'pool_pre_ping': True,            # Verifica conexiones activas
    'pool_recycle': 3600,             # Recicla conexiones (1 hora)
}
```

---

## 🚀 Inicialización

### 1. Inicializar Base de Datos (crear tablas)

```bash
python manage_db.py init
```

**Resultado:**

- ✓ Crea directorio `instance/`
- ✓ Crea archivo `billing_system.db`
- ✓ Crea todas las tablas

### 2. Cargar Datos de Prueba

```bash
python manage_db.py seed
```

**Incluye:**

- 3 clientes de ejemplo
- 5 productos de ejemplo
- 3 facturas de ejemplo
- 5 detalles de facturas
- 2 pagos de ejemplo

### 3. Ver Información de la BD

```bash
python manage_db.py info
```

**Salida:**

```
📊 Información de la Base de Datos
==================================================
Clientes:         3
Productos:        5
Facturas:         3
Pagos:            2
==================================================
```

### 4. Ver Esquema de la BD

```bash
python manage_db.py schema
```

**Muestra:**

- Todas las tablas
- Columnas de cada tabla
- Tipos de datos
- Restricciones (NULL/NOT NULL)

---

## 📚 Estructura de Modelos (Arquitectura MVC)

### Models (`app/models/`) - Capa M

Definen la estructura de datos con SQLAlchemy ORM:

```python
# app/models/customer.py
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    # ... más campos

    # Relación 1:N con facturas
    invoices = db.relationship('Invoice', backref='customer')
```

### Controllers (`app/controllers/`) - Capa C

Contienen la lógica de negocio:

```python
# app/controllers/customer_controller.py
class CustomerController:
    @staticmethod
    def create_customer(data):
        customer = Customer(name=data['name'], ...)
        db.session.add(customer)
        db.session.commit()
        return customer

    @staticmethod
    def get_all_customers():
        return Customer.query.all()
```

### Views (`app/views/`) - Capa V

Serializan modelos a JSON:

```python
# app/views/customer_view.py
class CustomerView:
    @staticmethod
    def serialize_customer(customer):
        return {
            'id': customer.id,
            'name': customer.name,
            'email': customer.email
        }
```

---

## 💻 Uso Práctico

### Ejecutar Aplicación

```bash
python run.py
```

Acceso: `http://localhost:5000`

### APIs Disponibles

#### Clientes

```bash
# Crear cliente
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -d '{"name":"Acme Corp","email":"contact@acme.com"}'

# Obtener todos
curl http://localhost:5000/api/customers

# Obtener uno
curl http://localhost:5000/api/customers/1

# Actualizar
curl -X PUT http://localhost:5000/api/customers/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Acme Corp Actualizada"}'

# Eliminar
curl -X DELETE http://localhost:5000/api/customers/1
```

#### Productos

```bash
# Crear producto
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "code":"PROD001",
    "name":"Producto Premium",
    "price":499.99,
    "tax_percentage":21.0,
    "stock":100
  }'
```

#### Facturas

```bash
# Crear factura con detalles
curl -X POST http://localhost:5000/api/invoices \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_number":"INV-2024-001",
    "customer_id":1,
    "due_date":"2024-12-31",
    "details":[
      {
        "product_id":1,
        "quantity":2,
        "unit_price":499.99
      }
    ]
  }'

# Obtener factura con detalles y pagos
curl http://localhost:5000/api/invoices/1

# Emitir factura (draft -> issued)
curl -X PUT http://localhost:5000/api/invoices/1/issue
```

#### Pagos

```bash
# Registrar pago
curl -X POST http://localhost:5000/api/payments \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_id":1,
    "amount":999.98,
    "payment_method":"bank_transfer",
    "reference":"BANK-001"
  }'

# Obtener pagos de factura
curl http://localhost:5000/api/payments/invoice/1
```

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=app

# Tests específicos
pytest tests/test_models.py
```

### Test de Modelos Incluidos

- ✓ Creación de clientes
- ✓ Creación de productos
- ✓ Creación de facturas

---

## 🔄 Operaciones de Base de Datos

### Reiniciar BD (eliminar y recrear)

```bash
python manage_db.py reset
```

### Eliminar todas las tablas

```bash
python manage_db.py drop
```

⚠️ **ADVERTENCIA**: Esta operación es irreversible

---

## 📁 Ubicación de Archivos

### Base de Datos

```
Desarrollo:    instance/billing_system.db
Testing:       :memory: (no archivos)
Producción:    data/billing_system_prod.db
```

### Crear directorios si no existen

```bash
# Windows
mkdir instance
mkdir data

# Mac/Linux
mkdir -p instance data
```

---

## 🐛 Troubleshooting

### Error: "No such table: customers"

**Solución:** Inicializar base de datos

```bash
python manage_db.py init
```

### Error: "database is locked"

**Causa:** Múltiples conexiones simultáneas

**Solución:** Aumentar timeout en `config.py`

```python
'connect_args': {
    'timeout': 30,  # Aumentar a 30 segundos
}
```

### Error: "operational error: database disk image is malformed"

**Solución:** Eliminar y recrear BD

```bash
rm instance/billing_system.db
python manage_db.py init
python manage_db.py seed
```

### Port 5000 en uso

**Solución:** Usar puerto diferente

```bash
FLASK_RUN_PORT=5001 python run.py
```

### ImportError: No module named 'flask'

**Solución:** Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 📊 Relaciones de Base de Datos

```
CUSTOMER (1) ──────→ (N) INVOICE ──────→ (N) PAYMENT
                          ↓
                   (N) INVOICE_DETAIL
                          ↓
                     (M) PRODUCT
```

### Características:

- ✓ Relaciones de integridad referencial
- ✓ Cascadas de eliminación configuradas
- ✓ Timestamps automáticos (created_at, updated_at)
- ✓ Estados de factura (draft, issued, paid, cancelled)

---

## 🎯 Mejores Prácticas

### 1. Usar con Transacciones

```python
from app import create_app, db
from app.models import Customer

app = create_app()

with app.app_context():
    try:
        customer = Customer(name='Juan', email='juan@example.com')
        db.session.add(customer)
        db.session.commit()
        print(f"✓ Cliente creado: {customer.id}")
    except Exception as e:
        db.session.rollback()
        print(f"✗ Error: {e}")
```

### 2. Consultas Eficientes

```python
# ✗ Evitar: N+1 queries
customers = Customer.query.all()
for customer in customers:
    print(customer.invoices)  # Genera query por cada cliente

# ✓ Usar: Eager loading
customers = Customer.query.options(
    db.joinedload(Customer.invoices)
).all()
```

### 3. Validación de Datos

```python
from app.utils.validators import Validators

email = "user@example.com"
if not Validators.is_valid_email(email):
    raise ValueError("Email inválido")
```

---

## 📚 Recursos Adicionales

- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/14/orm/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## ✅ Checklist de Configuración

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Variables de entorno configuradas (`.env`)
- [ ] Base de datos inicializada (`python manage_db.py init`)
- [ ] Datos de prueba cargados (`python manage_db.py seed`)
- [ ] Aplicación ejecutándose (`python run.py`)
- [ ] APIs probadas con curl o Postman

---

**¡Sistema de Facturación Backend listo para usar! 🚀**
