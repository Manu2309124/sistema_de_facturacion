"""
Script para inicializar y gestionar la base de datos SQLite
"""
import os
import sys
from datetime import datetime, timedelta
from app import create_app
from app.database import db, init_db, create_tables, drop_all_tables, reset_database
from app.models import Customer, Product, Invoice, InvoiceDetail, Payment

# Obtener el entorno
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)


def init_database():
    """Inicializa la base de datos desde cero"""
    print(f"\n🔧 Inicializando base de datos en modo {env}...")
    with app.app_context():
        db.create_all()
        print("✓ Base de datos inicializada correctamente")


def seed_database():
    """Carga datos de prueba en la base de datos"""
    print("\n🌱 Cargando datos de prueba...")
    
    with app.app_context():
        # Verificar si ya existen datos
        if Customer.query.first():
            print("⚠ La base de datos ya contiene datos. Skipping seeding.")
            return
        
        # Crear clientes
        customers = [
            Customer(
                name='Juan García López',
                email='juan.garcia@example.com',
                phone='+34 912345678',
                address='Calle Principal 123',
                city='Madrid',
                country='España',
                tax_id='ES12345678A',
                status='active'
            ),
            Customer(
                name='María Rodríguez',
                email='maria.rodriguez@example.com',
                phone='+34 987654321',
                address='Av. de la República 456',
                city='Barcelona',
                country='España',
                tax_id='ES87654321B',
                status='active'
            ),
            Customer(
                name='TechCorp S.L.',
                email='contacto@techcorp.com',
                phone='+34 934567890',
                address='Calle Innovación 789',
                city='Valencia',
                country='España',
                tax_id='ES11223344C',
                status='active'
            )
        ]
        
        for customer in customers:
            db.session.add(customer)
        db.session.commit()
        print(f"✓ {len(customers)} clientes creados")
        
        # Crear productos
        products = [
            Product(
                code='PROD001',
                name='Consultoría de Software',
                description='Servicio de consultoría en desarrollo de software',
                price=150.0,
                tax_percentage=21.0,
                stock=1000,
                status='active'
            ),
            Product(
                code='PROD002',
                name='Diseño Web',
                description='Diseño y desarrollo de sitios web responsive',
                price=120.0,
                tax_percentage=21.0,
                stock=1000,
                status='active'
            ),
            Product(
                code='PROD003',
                name='Soporte Técnico (Mes)',
                description='Soporte técnico y mantenimiento mensual',
                price=300.0,
                tax_percentage=21.0,
                stock=500,
                status='active'
            ),
            Product(
                code='PROD004',
                name='Licencia Software',
                description='Licencia anual de software empresarial',
                price=500.0,
                tax_percentage=21.0,
                stock=100,
                status='active'
            ),
            Product(
                code='PROD005',
                name='Base de Datos',
                description='Servicio de hosting de base de datos',
                price=75.0,
                tax_percentage=21.0,
                stock=1000,
                status='active'
            )
        ]
        
        for product in products:
            db.session.add(product)
        db.session.commit()
        print(f"✓ {len(products)} productos creados")
        
        # Crear facturas
        invoices = [
            Invoice(
                invoice_number='INV-2024-001',
                customer_id=1,
                invoice_date=datetime.utcnow(),
                due_date=datetime.utcnow() + timedelta(days=30),
                status='issued'
            ),
            Invoice(
                invoice_number='INV-2024-002',
                customer_id=2,
                invoice_date=datetime.utcnow(),
                due_date=datetime.utcnow() + timedelta(days=15),
                status='draft'
            ),
            Invoice(
                invoice_number='INV-2024-003',
                customer_id=3,
                invoice_date=datetime.utcnow() - timedelta(days=5),
                due_date=datetime.utcnow() + timedelta(days=25),
                status='paid'
            )
        ]
        
        for invoice in invoices:
            db.session.add(invoice)
        db.session.commit()
        print(f"✓ {len(invoices)} facturas creadas")
        
        # Crear detalles de facturas
        details = [
            InvoiceDetail(
                invoice_id=1,
                product_id=1,
                quantity=8,
                unit_price=150.0,
                tax_percentage=21.0,
                line_total=1200.0
            ),
            InvoiceDetail(
                invoice_id=1,
                product_id=3,
                quantity=1,
                unit_price=300.0,
                tax_percentage=21.0,
                line_total=300.0
            ),
            InvoiceDetail(
                invoice_id=2,
                product_id=2,
                quantity=1,
                unit_price=120.0,
                tax_percentage=21.0,
                line_total=120.0
            ),
            InvoiceDetail(
                invoice_id=3,
                product_id=4,
                quantity=2,
                unit_price=500.0,
                tax_percentage=21.0,
                line_total=1000.0
            ),
            InvoiceDetail(
                invoice_id=3,
                product_id=5,
                quantity=3,
                unit_price=75.0,
                tax_percentage=21.0,
                line_total=225.0
            )
        ]
        
        for detail in details:
            db.session.add(detail)
        db.session.commit()
        
        # Recalcular totales de facturas
        for invoice in invoices:
            subtotal = sum(d.line_total for d in invoice.invoice_details)
            tax = sum(d.line_total * d.tax_percentage / 100 for d in invoice.invoice_details)
            invoice.subtotal = subtotal
            invoice.tax_amount = tax
            invoice.total_amount = subtotal + tax
        db.session.commit()
        print(f"✓ {len(details)} detalles de factura creados")
        
        # Crear pagos
        payments = [
            Payment(
                invoice_id=1,
                payment_date=datetime.utcnow(),
                amount=726.0,
                payment_method='bank_transfer',
                reference='BANK-001',
                notes='Pago parcial'
            ),
            Payment(
                invoice_id=3,
                payment_date=datetime.utcnow() - timedelta(days=2),
                amount=1481.25,
                payment_method='credit_card',
                reference='CC-4242',
                notes='Pago completo'
            )
        ]
        
        for payment in payments:
            db.session.add(payment)
        db.session.commit()
        print(f"✓ {len(payments)} pagos creados")


def show_database_info():
    """Muestra información de la base de datos"""
    print(f"\n📊 Información de la Base de Datos")
    print(f"{'='*50}")
    
    with app.app_context():
        # Contar registros
        customers_count = Customer.query.count()
        products_count = Product.query.count()
        invoices_count = Invoice.query.count()
        payments_count = Payment.query.count()
        
        print(f"Clientes:         {customers_count}")
        print(f"Productos:        {products_count}")
        print(f"Facturas:         {invoices_count}")
        print(f"Pagos:            {payments_count}")
        print(f"{'='*50}\n")


def export_database_schema():
    """Exporta el esquema de la base de datos"""
    print("\n📋 Esquema de la Base de Datos")
    print("="*70)
    
    with app.app_context():
        from sqlalchemy import inspect, MetaData
        
        inspector = inspect(db.engine)
        table_names = inspector.get_table_names()
        
        for table_name in sorted(table_names):
            columns = inspector.get_columns(table_name)
            print(f"\n📌 Tabla: {table_name}")
            print("-" * 70)
            for column in columns:
                col_type = str(column['type'])
                nullable = "NULL" if column['nullable'] else "NOT NULL"
                print(f"  • {column['name']:<20} {col_type:<20} {nullable}")
            print()


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("GESTOR DE BASE DE DATOS - SISTEMA DE FACTURACIÓN")
    print("="*70)
    
    if len(sys.argv) < 2:
        print("\nUso: python manage_db.py [comando]")
        print("\nComandos disponibles:")
        print("  init      - Inicializa la base de datos")
        print("  seed      - Carga datos de prueba")
        print("  info      - Muestra información de la BD")
        print("  schema    - Exporta el esquema de la BD")
        print("  reset     - Reinicia la BD (elimina y crea tablas)")
        print("  drop      - Elimina todas las tablas (¡CUIDADO!)")
        print("="*70 + "\n")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'init':
        init_database()
    elif command == 'seed':
        init_database()
        seed_database()
    elif command == 'info':
        show_database_info()
    elif command == 'schema':
        export_database_schema()
    elif command == 'reset':
        print("\n⚠ ADVERTENCIA: Se eliminarán todas las tablas")
        confirm = input("¿Estás seguro? (s/n): ").lower()
        if confirm == 's':
            reset_database(app)
            seed_database()
    elif command == 'drop':
        print("\n⚠ ADVERTENCIA CRÍTICA: Se eliminarán permanentemente todas las tablas")
        confirm = input("¿Estás COMPLETAMENTE seguro? (escribir 'SI'): ")
        if confirm == 'SI':
            drop_all_tables(app)
    else:
        print(f"\n❌ Comando desconocido: {command}")
    
    print()


if __name__ == '__main__':
    main()
