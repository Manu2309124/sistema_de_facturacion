# Quick Start - Sistema de Facturación Backend

## ⚡ Configuración en 5 minutos

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

### 3. Inicializar base de datos

```bash
# Crear tablas
python manage_db.py init

# Cargar datos de prueba
python manage_db.py seed

# Ver información
python manage_db.py info
```

### 4. Ejecutar servidor

```bash
python run.py
```

### 5. Probar API

```bash
# Ver todos los clientes
curl http://localhost:5000/api/customers

# Crear cliente
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com"}'
```

---

## 📚 Comandos Principales

### Gestión de BD

```bash
python manage_db.py init          # Crear tablas
python manage_db.py seed          # Cargar datos de prueba
python manage_db.py info          # Ver información
python manage_db.py schema        # Ver esquema de tablas
python manage_db.py reset         # Reiniciar BD
python manage_db.py drop          # Eliminar todo (⚠️ CUIDADO)
```

### Flask Shell (Python REPL)

```bash
python -m flask shell

>>> from app.models import Customer
>>> customers = Customer.query.all()
>>> for c in customers: print(c.name)
```

### Tests

```bash
pytest                       # Todos
pytest --cov=app            # Con cobertura
pytest tests/test_models.py # Específicos
```

---

## 🔗 Endpoints de la API

### Clientes

- `GET /api/customers` - Obtener todos
- `POST /api/customers` - Crear
- `GET /api/customers/<id>` - Obtener uno
- `PUT /api/customers/<id>` - Actualizar
- `DELETE /api/customers/<id>` - Eliminar

### Productos

- `GET /api/products` - Obtener todos
- `POST /api/products` - Crear
- `GET /api/products/<id>` - Obtener uno
- `PUT /api/products/<id>` - Actualizar
- `DELETE /api/products/<id>` - Eliminar

### Facturas

- `GET /api/invoices` - Obtener todas
- `POST /api/invoices` - Crear
- `GET /api/invoices/<id>` - Obtener una
- `PUT /api/invoices/<id>` - Actualizar
- `PUT /api/invoices/<id>/issue` - Emitir
- `DELETE /api/invoices/<id>` - Eliminar

### Pagos

- `GET /api/payments/invoice/<id>` - Pagos de factura
- `POST /api/payments` - Crear pago
- `GET /api/payments/<id>` - Obtener pago
- `DELETE /api/payments/<id>` - Eliminar pago

---

## 📁 Archivos Importantes

- `app/config.py` - Configuración por entorno
- `app/database.py` - Inicialización de BD
- `manage_db.py` - Gestión de BD
- `run.py` - Punto de entrada
- `requirements.txt` - Dependencias
- `.env` - Variables de entorno

---

## 🎯 Documentación Completa

- [SQLITE_SETUP.md](SQLITE_SETUP.md) - Guía detallada de configuración
- [SQLITE_CONFIG.md](SQLITE_CONFIG.md) - Información técnica de SQLite
- [EJEMPLOS_USO.md](EJEMPLOS_USO.md) - Ejemplos de uso y API

---

## ✅ Verificación

```bash
# Verificar que todo funciona
python run.py

# En otra terminal:
curl http://localhost:5000/api/customers
```

Si ves datos de clientes, ¡está funcionando! 🚀

---

## 🆘 Problemas Comunes

### "No such table: customers"

```bash
python manage_db.py init
```

### "Address already in use"

```bash
FLASK_RUN_PORT=5001 python run.py
```

### "database is locked"

Aumentar timeout en `app/config.py` (línea 36):

```python
'timeout': 30,  # Aumentar a 30 segundos
```

---

**¡Sistema listo para usar!** 🎉
