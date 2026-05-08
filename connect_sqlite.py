#!/usr/bin/env python
"""Script para conectarse a SQLite e interactuar con los datos"""
from app import create_app
from app.models import Customer, Product, Invoice, Payment
from app.database import db

app = create_app('development')

with app.app_context():
    print("\n" + "="*70)
    print("✓ CONECTADO A SQLITE - SISTEMA DE FACTURACIÓN")
    print("="*70)
    
    print("\n📋 CLIENTES EN LA BD:")
    print("-" * 70)
    customers = Customer.query.all()
    for customer in customers:
        print(f"  {customer.id}. {customer.name}")
        print(f"     Email: {customer.email}")
        print(f"     Tax ID: {customer.tax_id}")
        print(f"     Teléfono: {customer.phone}")
        print()
    
    print("\n📦 PRODUCTOS EN LA BD:")
    print("-" * 70)
    products = Product.query.all()
    for product in products:
        print(f"  {product.id}. {product.code} - {product.name}")
        print(f"     Precio: ${product.price}")
        print(f"     Impuesto: {product.tax_percentage}%")
        print(f"     Stock: {product.stock} unidades")
        print()
    
    print("\n📄 FACTURAS EN LA BD:")
    print("-" * 70)
    invoices = Invoice.query.all()
    for invoice in invoices:
        customer = Customer.query.get(invoice.customer_id)
        print(f"  {invoice.id}. {invoice.invoice_number}")
        print(f"     Cliente: {customer.name}")
        print(f"     Subtotal: ${invoice.subtotal}")
        print(f"     Impuestos: ${invoice.tax_amount}")
        print(f"     Total: ${invoice.total_amount}")
        print(f"     Estado: {invoice.status}")
        print()
    
    print("\n💳 PAGOS EN LA BD:")
    print("-" * 70)
    payments = Payment.query.all()
    if payments:
        for payment in payments:
            invoice = Invoice.query.get(payment.invoice_id)
            print(f"  {payment.id}. Factura #{invoice.invoice_number}")
            print(f"     Monto: ${payment.amount}")
            print(f"     Método: {payment.payment_method}")
            print(f"     Referencia: {payment.reference}")
            print(f"     Fecha: {payment.payment_date}")
            print()
    else:
        print("  No hay pagos registrados")
        print()
    
    print("\n📊 ESTADÍSTICAS:")
    print("-" * 70)
    print(f"  Total de Clientes: {Customer.query.count()}")
    print(f"  Total de Productos: {Product.query.count()}")
    print(f"  Total de Facturas: {Invoice.query.count()}")
    print(f"  Total de Pagos: {Payment.query.count()}")
    
    # Calcular ingresos totales
    total_invoiced = db.session.query(db.func.sum(Invoice.total_amount)).scalar() or 0
    total_paid = db.session.query(db.func.sum(Payment.amount)).scalar() or 0
    
    print(f"  Total Facturado: ${total_invoiced}")
    print(f"  Total Pagado: ${total_paid}")
    print(f"  Pendiente: ${total_invoiced - total_paid}")
    
    print("\n" + "="*70)
    print("✓ BASE DE DATOS SQLITE LISTA PARA USAR")
    print("="*70 + "\n")
