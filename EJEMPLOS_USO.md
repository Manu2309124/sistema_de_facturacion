"""
Ejemplos de uso del Sistema de Facturación Backend
Comandos para terminal, curl y pruebas
"""

# ============================================================================

# 1. INICIAR EL SERVIDOR

# ============================================================================

# Terminal - Iniciar en modo desarrollo

python run.py

# Terminal - Iniciar en modo testing

set FLASK_ENV=testing && python run.py

# Terminal - Iniciar en puerto diferente

set FLASK_RUN_PORT=5001 && python run.py

# ============================================================================

# 2. GESTIÓN DE BASE DE DATOS

# ============================================================================

# Inicializar BD (crear tablas vacías)

python manage_db.py init

# Inicializar + cargar datos de prueba

python manage_db.py seed

# Ver información de BD

python manage_db.py info

# Ver esquema de tablas

python manage_db.py schema

# Reiniciar BD (elimina y recrea todo)

python manage_db.py reset

# Eliminar todas las tablas

python manage_db.py drop

# ============================================================================

# 3. API CLIENTES

# ============================================================================

# CREAR cliente

curl -X POST http://localhost:5000/api/customers ^
-H "Content-Type: application/json" ^
-d "{\"name\":\"Acme Corp\",\"email\":\"contact@acme.com\",\"phone\":\"+34 912345678\",\"address\":\"Calle 123\",\"city\":\"Madrid\",\"country\":\"España\",\"tax_id\":\"ES12345678A\"}"

# OBTENER todos los clientes

curl http://localhost:5000/api/customers

# OBTENER cliente específico

curl http://localhost:5000/api/customers/1

# ACTUALIZAR cliente

curl -X PUT http://localhost:5000/api/customers/1 ^
-H "Content-Type: application/json" ^
-d "{\"name\":\"Acme Corp - Actualizado\",\"city\":\"Valencia\"}"

# ELIMINAR cliente

curl -X DELETE http://localhost:5000/api/customers/1

# ============================================================================

# 4. API PRODUCTOS

# ============================================================================

# CREAR producto

curl -X POST http://localhost:5000/api/products ^
-H "Content-Type: application/json" ^
-d "{\"code\":\"PROD-001\",\"name\":\"Consultoría Premium\",\"description\":\"Servicio de consultoría empresarial\",\"price\":500.0,\"tax_percentage\":21.0,\"stock\":50}"

# OBTENER todos los productos

curl http://localhost:5000/api/products

# OBTENER producto específico

curl http://localhost:5000/api/products/1

# ACTUALIZAR producto (aumentar precio)

curl -X PUT http://localhost:5000/api/products/1 ^
-H "Content-Type: application/json" ^
-d "{\"price\":550.0,\"stock\":45}"

# ELIMINAR producto

curl -X DELETE http://localhost:5000/api/products/1

# ============================================================================

# 5. API FACTURAS

# ============================================================================

# CREAR factura (simple)

curl -X POST http://localhost:5000/api/invoices ^
-H "Content-Type: application/json" ^
-d "{\"invoice_number\":\"INV-2024-001\",\"customer_id\":1,\"due_date\":\"2024-12-31\",\"details\":[]}"

# CREAR factura (con detalles)

curl -X POST http://localhost:5000/api/invoices ^
-H "Content-Type: application/json" ^
-d "{\"invoice_number\":\"INV-2024-002\",\"customer_id\":1,\"due_date\":\"2024-12-31\",\"details\":[{\"product_id\":1,\"quantity\":3,\"unit_price\":500.0},{\"product_id\":2,\"quantity\":1,\"unit_price\":120.0}]}"

# OBTENER todas las facturas

curl http://localhost:5000/api/invoices

# OBTENER factura con detalles y pagos

curl http://localhost:5000/api/invoices/1

# ACTUALIZAR factura (cambiar fecha vencimiento)

curl -X PUT http://localhost:5000/api/invoices/1 ^
-H "Content-Type: application/json" ^
-d "{\"due_date\":\"2025-01-15\",\"notes\":\"Factura actualizada\"}"

# EMITIR factura (cambiar status draft -> issued)

curl -X PUT http://localhost:5000/api/invoices/1/issue

# ELIMINAR factura

curl -X DELETE http://localhost:5000/api/invoices/1

# ============================================================================

# 6. API PAGOS

# ============================================================================

# REGISTRAR pago

curl -X POST http://localhost:5000/api/payments ^
-H "Content-Type: application/json" ^
-d "{\"invoice_id\":1,\"amount\":1000.0,\"payment_method\":\"bank_transfer\",\"reference\":\"BANK-001-2024\",\"notes\":\"Pago parcial\"}"

# OBTENER pago específico

curl http://localhost:5000/api/payments/1

# OBTENER todos los pagos de una factura

curl http://localhost:5000/api/payments/invoice/1

# ELIMINAR pago

curl -X DELETE http://localhost:5000/api/payments/1

# ============================================================================

# 7. PRUEBAS CON PYTHON

# ============================================================================

# Ejecutar todos los tests

pytest

# Tests con cobertura

pytest --cov=app

# Tests de un archivo específico

pytest tests/test_models.py

# Tests verbose (con detalle)

pytest -v

# ============================================================================

# 8. USAR FLASK SHELL (REPL INTERACTIVO)

# ============================================================================

# Iniciar shell de Flask

python -m flask shell

# Dentro del shell:

# Importar modelos

> > > from app.models import Customer, Product, Invoice, Payment
> > > from app.database import db

# Crear un cliente

> > > customer = Customer(name='Test User', email='test@example.com')
> > > db.session.add(customer)
> > > db.session.commit()
> > > print(customer.id)
> > > 1

# Consultar clientes

> > > customers = Customer.query.all()
> > > for c in customers:
> > > ... print(f"{c.id}: {c.name}")

# Crear producto

> > > product = Product(code='TEST', name='Test Product', price=99.99, tax_percentage=21.0)
> > > db.session.add(product)
> > > db.session.commit()

# Actualizar

> > > customer = Customer.query.first()
> > > customer.city = 'Madrid'
> > > db.session.commit()

# Eliminar

> > > customer = Customer.query.first()
> > > db.session.delete(customer)
> > > db.session.commit()

# Salir del shell

> > > exit()

# ============================================================================

# 9. EJEMPLOS PRÁCTICOS COMPLETOS

# ============================================================================

# --- ESCENARIO 1: Crear un cliente y factura completa ---

# 1. Inicializar BD

python manage_db.py init

# 2. Crear cliente

curl -X POST http://localhost:5000/api/customers ^
-H "Content-Type: application/json" ^
-d "{\"name\":\"Tech Solutions\",\"email\":\"admin@techsolutions.com\",\"tax_id\":\"ES99999999Z\"}"

# Respuesta: {"id": 1, ...}

# 3. Crear productos

curl -X POST http://localhost:5000/api/products ^
-H "Content-Type: application/json" ^
-d "{\"code\":\"SRV-001\",\"name\":\"Desarrollo Web\",\"price\":1500.0,\"tax_percentage\":21.0}"

# Respuesta: {"id": 1, ...}

curl -X POST http://localhost:5000/api/products ^
-H "Content-Type: application/json" ^
-d "{\"code\":\"SRV-002\",\"name\":\"Mantenimiento\",\"price\":500.0,\"tax_percentage\":21.0}"

# Respuesta: {"id": 2, ...}

# 4. Crear factura con detalles

curl -X POST http://localhost:5000/api/invoices ^
-H "Content-Type: application/json" ^
-d "{\"invoice_number\":\"INV-2024-TECH-001\",\"customer_id\":1,\"due_date\":\"2024-12-31\",\"details\":[{\"product_id\":1,\"quantity\":1,\"unit_price\":1500.0},{\"product_id\":2,\"quantity\":3,\"unit_price\":500.0}]}"

# Respuesta: Factura con totales calculados

# 5. Emitir factura

curl -X PUT http://localhost:5000/api/invoices/1/issue

# 6. Registrar pagos

curl -X POST http://localhost:5000/api/payments ^
-H "Content-Type: application/json" ^
-d "{\"invoice_id\":1,\"amount\":1210.0,\"payment_method\":\"credit_card\",\"reference\":\"CC-VISA-2024\"}"

curl -X POST http://localhost:5000/api/payments ^
-H "Content-Type: application/json" ^
-d "{\"invoice_id\":1,\"amount\":1210.0,\"payment_method\":\"bank_transfer\",\"reference\":\"TRANSFER-001\"}"

# 7. Ver factura completamente pagada

curl http://localhost:5000/api/invoices/1

# ============================================================================

# 10. ESTRUCTURAS JSON DE EJEMPLO

# ============================================================================

# --- Cliente completo ---

{
"id": 1,
"name": "Acme Corporation",
"email": "contact@acme.com",
"phone": "+34 912345678",
"address": "Calle Principal 123",
"city": "Madrid",
"country": "España",
"tax_id": "ES12345678Z",
"status": "active",
"created_at": "2024-05-08T10:30:00",
"updated_at": "2024-05-08T10:30:00"
}

# --- Producto completo ---

{
"id": 1,
"code": "PROD-001",
"name": "Consultoría de Software",
"description": "Servicio de consultoría empresarial",
"price": 500.0,
"tax_percentage": 21.0,
"stock": 100,
"status": "active",
"created_at": "2024-05-08T10:30:00",
"updated_at": "2024-05-08T10:30:00"
}

# --- Factura con detalles ---

{
"id": 1,
"invoice_number": "INV-2024-001",
"customer_id": 1,
"invoice_date": "2024-05-08T10:30:00",
"due_date": "2024-06-08T00:00:00",
"subtotal": 1500.0,
"tax_amount": 315.0,
"total_amount": 1815.0,
"status": "issued",
"notes": "Factura de servicios",
"created_at": "2024-05-08T10:30:00",
"updated_at": "2024-05-08T10:30:00",
"details": [
{
"id": 1,
"product_name": "Consultoría de Software",
"quantity": 3,
"unit_price": 500.0,
"tax_percentage": 21.0,
"line_total": 1500.0
}
],
"payments": [
{
"id": 1,
"amount": 1815.0,
"payment_method": "bank_transfer",
"payment_date": "2024-05-08T10:30:00"
}
]
}

# --- Pago completo ---

{
"id": 1,
"invoice_id": 1,
"payment_date": "2024-05-08T10:30:00",
"amount": 500.0,
"payment_method": "credit_card",
"reference": "CC-4242",
"notes": "Pago inicial",
"created_at": "2024-05-08T10:30:00",
"updated_at": "2024-05-08T10:30:00"
}
