"""
Configuración de SQLite con Flask SQLAlchemy
Guía completa de instalación y uso
"""

import os
from flask import Flask
from app.database import db, init_db
from app.config import config

def create_app(config_name='development'):
"""
Factory function para crear la aplicación Flask

    Arquitectura MVC:
    - Models: app/models/
    - Views: app/views/ (serializadores JSON)
    - Controllers: app/controllers/ (lógica de negocio)

    Args:
        config_name (str): Nombre de la configuración (development, testing, production)

    Returns:
        Flask: Instancia de aplicación Flask
    """
    # Crear aplicación
    app = Flask(__name__)

    # Cargar configuración
    app.config.from_object(config[config_name])

    # Crear directorio de instancia si no existe
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Crear directorio de datos para producción
    if config_name == 'production':
        data_dir = os.path.join(os.path.dirname(app.root_path), 'data')
        os.makedirs(data_dir, exist_ok=True)

    # Inicializar base de datos
    init_db(app)

    # Registrar blueprints (rutas)
    with app.app_context():
        from app.controllers.invoice_controller import invoice_bp
        from app.controllers.customer_controller import customer_bp
        from app.controllers.product_controller import product_bp
        from app.controllers.payment_controller import payment_bp

        app.register_blueprint(invoice_bp, url_prefix='/api/invoices')
        app.register_blueprint(customer_bp, url_prefix='/api/customers')
        app.register_blueprint(product_bp, url_prefix='/api/products')
        app.register_blueprint(payment_bp, url_prefix='/api/payments')

    # Crear tablas en el contexto de aplicación
    with app.app_context():
        db.create_all()

    return app

# ============================================================================

# CONFIGURACIÓN DE SQLite

# ============================================================================

"""
SQLite con Flask-SQLAlchemy es ideal para:

- Desarrollo local
- Pruebas unitarias
- Aplicaciones pequeñas/medianas
- Prototipos rápidos

Características de la configuración:

1. DESARROLLO (SQLite en archivo)
   - Base de datos: billing_system.db
   - Ubicación: instance/billing_system.db
   - Echo SQL: True (muestra todas las queries)
   - Timeout: 15 segundos

2. TESTING (SQLite en memoria)
   - Base de datos: :memory:
   - Rápido y aislado
   - No necesita limpieza de archivos
   - Perfecto para tests

3. PRODUCCIÓN (SQLite optimizado)
   - Base de datos: billing_system_prod.db
   - Ubicación: data/billing_system_prod.db
   - Timeout: 30 segundos
   - Pool optimizado (size=10, max_overflow=20)

Opciones de conexión SQLite:

- timeout: Tiempo máximo de espera de bloqueo BD
- check_same_thread: Permite múltiples threads
- pool_pre_ping: Verifica conexiones activas
- pool_recycle: Recicla conexiones antiguas
  """

# ============================================================================

# ESTRUCTURA DE DIRECTORIOS

# ============================================================================

"""
prompting/
├── app/
│ ├── controllers/ # Lógica de negocio (MVC: C)
│ │ ├── **init**.py
│ │ ├── customer_controller.py
│ │ ├── product_controller.py
│ │ ├── invoice_controller.py
│ │ └── payment_controller.py
│ │
│ ├── models/ # Modelos de datos (MVC: M)
│ │ ├── **init**.py
│ │ ├── customer.py # db.Model
│ │ ├── product.py # db.Model
│ │ ├── invoice.py # db.Model
│ │ ├── invoice_detail.py # db.Model
│ │ └── payment.py # db.Model
│ │
│ ├── views/ # Serializadores JSON (MVC: V)
│ │ ├── **init**.py
│ │ ├── customer_view.py
│ │ ├── product_view.py
│ │ ├── invoice_view.py
│ │ └── payment_view.py
│ │
│ ├── utils/ # Utilidades
│ │ ├── decorators.py # Decoradores personalizados
│ │ └── validators.py # Validaciones
│ │
│ ├── **init**.py # Factory de aplicación
│ ├── config.py # Configuración por entorno
│ └── database.py # Inicialización SQLAlchemy
│
├── instance/ # Instancia de aplicación (archivo .db)
│ └── billing_system.db # Base de datos SQLite desarrollo
│
├── data/ # Datos para producción
│ └── billing_system_prod.db # Base de datos SQLite producción
│
├── manage_db.py # Gestión de BD
├── run.py # Punto de entrada
├── requirements.txt # Dependencias
└── .env # Variables de entorno
"""

# ============================================================================

# FLUJO DE CONFIGURACIÓN

# ============================================================================

"""

1. INSTALACIÓN
   $ pip install -r requirements.txt

2. CONFIGURAR VARIABLES DE ENTORNO (.env)
   FLASK_APP=run.py
   FLASK_ENV=development
   DATABASE_URL=sqlite:///instance/billing_system.db

3. INICIALIZAR BASE DE DATOS
   $ python manage_db.py init # Crear tablas
   $ python manage_db.py seed # Cargar datos de prueba
   $ python manage_db.py info # Ver información

4. EJECUTAR APLICACIÓN
   $ python run.py # En http://localhost:5000

5. ACCEDER A LA API
   GET http://localhost:5000/api/customers
   POST http://localhost:5000/api/customers
   GET http://localhost:5000/api/customers/1
   etc.
   """

# ============================================================================

# RELACIONES ENTRE MODELOS

# ============================================================================

"""
Diagrama ER (Entidad-Relación):

┌─────────────┐
│ CUSTOMER │
├─────────────┤
│ id (PK) │◄──────┐
│ name │ │ (1:N)
│ email │ │
│ tax_id │ │
└─────────────┘ │
│
┌─────────────┐
│ INVOICE │
├─────────────┤
│ id (PK) │
│ customer_id │──────────────────────────┐
│ invoice_num │ │ (1:N)
│ total │ │
└─────────────┘ │
│ │
│ (1:N) │
│ ┌─────────────────┐
└──────────────────────────┤ INVOICE_DETAIL │
├─────────────────┤
┌───────────────────────────►│ invoice_id (FK) │
│ (N:1) │ product_id (FK) │
│ │ quantity │
┌──────────┐ │ line_total │
│ PRODUCT │ └─────────────────┘
├──────────┤
│ id (PK) │
│ code │
│ price │
│ tax_pct │
│ stock │
└──────────┘

              ┌──────────┐
              │ PAYMENT  │
              ├──────────┤
              │ id (PK)  │
              │ invoice_ │──────────┐
              │   id     │          │ (N:1)
              │ amount   │          │
              │ method   │    ┌─────────────┐
              │ ref      │    │   INVOICE   │
              └──────────┘    └─────────────┘

"""

# ============================================================================

# EJEMPLO DE USO PRÁCTICO

# ============================================================================

"""

1. INICIALIZAR BASE DE DATOS:
   $ python manage_db.py seed
2. CREAR UN CLIENTE:
   $ curl -X POST http://localhost:5000/api/customers \\
   -H "Content-Type: application/json" \\
   -d '{
   "name": "Acme Corp",
   "email": "contact@acme.com",
   "phone": "+34 912345678",
   "address": "Calle 123",
   "city": "Madrid",
   "country": "España",
   "tax_id": "ES12345678Z"
   }'

3. CREAR UN PRODUCTO:
   $ curl -X POST http://localhost:5000/api/products \\
   -H "Content-Type: application/json" \\
   -d '{
   "code": "PROD001",
   "name": "Servicio Premium",
   "price": 499.99,
   "tax_percentage": 21.0,
   "stock": 100
   }'

4. CREAR UNA FACTURA:
   $ curl -X POST http://localhost:5000/api/invoices \\
   -H "Content-Type: application/json" \\
   -d '{
   "invoice_number": "INV-2024-001",
   "customer_id": 1,
   "due_date": "2024-12-31",
   "details": [
   {
   "product_id": 1,
   "quantity": 3,
   "unit_price": 499.99
   }
   ]
   }'

5. REGISTRAR UN PAGO:
   $ curl -X POST http://localhost:5000/api/payments \\
   -H "Content-Type: application/json" \\
   -d '{
   "invoice_id": 1,
   "amount": 1499.97,
   "payment_method": "credit_card",
   "reference": "CC-4242"
   }'
   """
