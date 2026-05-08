# Sistema de Facturación Backend

Un sistema de facturación backend desarrollado con **Python**, **Flask** y arquitectura **MVC** (Model-View-Controller).

## Características

- ✅ Gestión de clientes
- ✅ Gestión de productos
- ✅ Creación de facturas
- ✅ Detalles de facturas
- ✅ Registro de pagos
- ✅ API RESTful
- ✅ Base de datos SQLAlchemy

## Requisitos

- Python 3.8+
- pip

## Instalación

1. **Clonar el repositorio**

```bash
git clone <repository-url>
cd prompting
```

2. **Crear entorno virtual**

```bash
python -m venv venv
source venv/Scripts/activate  # En Windows
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
   Editar el archivo `.env` con tu configuración

5. **Ejecutar la aplicación**

```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## Estructura del Proyecto

```
prompting/
├── app/
│   ├── controllers/          # Lógica de negocio
│   │   ├── customer_controller.py
│   │   ├── product_controller.py
│   │   ├── invoice_controller.py
│   │   └── payment_controller.py
│   ├── models/               # Modelos de datos
│   │   ├── customer.py
│   │   ├── product.py
│   │   ├── invoice.py
│   │   ├── invoice_detail.py
│   │   └── payment.py
│   ├── views/                # Serializadores de respuestas
│   │   ├── customer_view.py
│   │   ├── product_view.py
│   │   ├── invoice_view.py
│   │   └── payment_view.py
│   ├── utils/                # Utilidades
│   │   ├── decorators.py
│   │   └── validators.py
│   ├── config.py             # Configuración
│   ├── database.py           # Conexión a BD
│   └── __init__.py           # Factory de aplicación
├── migrations/               # Migraciones de BD
├── tests/                    # Tests unitarios
├── run.py                    # Punto de entrada
├── requirements.txt          # Dependencias
├── .env                      # Variables de entorno
└── README.md                 # Este archivo
```

## Endpoints de la API

### Clientes

- `POST /api/customers` - Crear cliente
- `GET /api/customers` - Obtener todos
- `GET /api/customers/<id>` - Obtener por ID
- `PUT /api/customers/<id>` - Actualizar
- `DELETE /api/customers/<id>` - Eliminar

### Productos

- `POST /api/products` - Crear producto
- `GET /api/products` - Obtener todos
- `GET /api/products/<id>` - Obtener por ID
- `PUT /api/products/<id>` - Actualizar
- `DELETE /api/products/<id>` - Eliminar

### Facturas

- `POST /api/invoices` - Crear factura
- `GET /api/invoices` - Obtener todas
- `GET /api/invoices/<id>` - Obtener por ID
- `PUT /api/invoices/<id>` - Actualizar
- `DELETE /api/invoices/<id>` - Eliminar
- `PUT /api/invoices/<id>/issue` - Emitir factura

### Pagos

- `POST /api/payments` - Registrar pago
- `GET /api/payments/<id>` - Obtener pago
- `GET /api/payments/invoice/<invoice_id>` - Pagos de factura
- `DELETE /api/payments/<id>` - Eliminar pago

## Ejemplo de Uso

### Crear Cliente

```bash
curl -X POST http://localhost:5000/api/customers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan García",
    "email": "juan@example.com",
    "phone": "1234567890",
    "address": "Calle Principal 123",
    "city": "Madrid",
    "country": "España",
    "tax_id": "ES12345678Z"
  }'
```

### Crear Producto

```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "code": "PROD001",
    "name": "Producto Ejemplo",
    "description": "Descripción del producto",
    "price": 99.99,
    "tax_percentage": 21.0,
    "stock": 100
  }'
```

### Crear Factura

```bash
curl -X POST http://localhost:5000/api/invoices \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_number": "INV001",
    "customer_id": 1,
    "due_date": "2024-01-15",
    "details": [
      {
        "product_id": 1,
        "quantity": 2,
        "unit_price": 99.99
      }
    ]
  }'
```

## Testing

Ejecutar tests:

```bash
pytest tests/
```

Con cobertura:

```bash
pytest --cov=app tests/
```

## Configuración

El archivo `.env` contiene:

- `FLASK_APP`: Punto de entrada
- `FLASK_ENV`: Entorno (development/testing/production)
- `SECRET_KEY`: Clave secreta
- `DATABASE_URL`: URL de conexión a BD

## Arquitectura MVC

- **Models**: Definen la estructura de datos (`app/models/`)
- **Views**: Serializan las respuestas JSON (`app/views/`)
- **Controllers**: Contienen la lógica de negocio (`app/controllers/`)

## Próximas mejoras

- [ ] Autenticación y autorización
- [ ] Generación de PDFs
- [ ] Sistema de roles
- [ ] Historial de cambios
- [ ] Reportes avanzados

## Licencia

MIT

## Autor

Sistema de Facturación
