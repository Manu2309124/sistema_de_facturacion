from flask import Blueprint, request, jsonify
from app.database import db
from app.models.invoice import Invoice
from app.models.invoice_detail import InvoiceDetail
from app.models.customer import Customer
from app.models.product import Product
from app.views.invoice_view import InvoiceView

invoice_bp = Blueprint('invoices', __name__)

class InvoiceController:
    """Business logic for invoices"""
    
    @staticmethod
    def create_invoice(data):
        """Create a new invoice"""
        customer = Customer.query.get(data.get('customer_id'))
        if not customer:
            return {'error': 'Customer not found'}, 404
        
        invoice = Invoice(
            invoice_number=data.get('invoice_number'),
            customer_id=data.get('customer_id'),
            due_date=data.get('due_date'),
            notes=data.get('notes')
        )
        
        db.session.add(invoice)
        db.session.flush()
        
        # Add invoice details
        details = data.get('details', [])
        for detail in details:
            product = Product.query.get(detail.get('product_id'))
            if not product:
                db.session.rollback()
                return {'error': f"Product {detail.get('product_id')} not found"}, 404
            
            invoice_detail = InvoiceDetail(
                invoice_id=invoice.id,
                product_id=detail.get('product_id'),
                quantity=detail.get('quantity'),
                unit_price=detail.get('unit_price', product.price),
                tax_percentage=product.tax_percentage,
                line_total=float(detail.get('quantity')) * float(detail.get('unit_price', product.price))
            )
            db.session.add(invoice_detail)
        
        # Calculate totals
        InvoiceController._calculate_totals(invoice)
        
        db.session.commit()
        return InvoiceView.serialize_invoice_with_details(invoice), 201
    
    @staticmethod
    def get_invoice(invoice_id):
        """Get invoice by ID"""
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return {'error': 'Invoice not found'}, 404
        return InvoiceView.serialize_invoice_with_details(invoice), 200
    
    @staticmethod
    def get_all_invoices():
        """Get all invoices"""
        invoices = Invoice.query.all()
        return InvoiceView.serialize_invoices(invoices), 200
    
    @staticmethod
    def update_invoice(invoice_id, data):
        """Update invoice"""
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return {'error': 'Invoice not found'}, 404
        
        if invoice.status != 'draft':
            return {'error': 'Can only edit draft invoices'}, 400
        
        invoice.due_date = data.get('due_date', invoice.due_date)
        invoice.notes = data.get('notes', invoice.notes)
        
        db.session.commit()
        return InvoiceView.serialize_invoice_with_details(invoice), 200
    
    @staticmethod
    def delete_invoice(invoice_id):
        """Delete invoice"""
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return {'error': 'Invoice not found'}, 404
        
        db.session.delete(invoice)
        db.session.commit()
        return {'message': 'Invoice deleted'}, 200
    
    @staticmethod
    def issue_invoice(invoice_id):
        """Change invoice status to issued"""
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return {'error': 'Invoice not found'}, 404
        
        invoice.status = 'issued'
        db.session.commit()
        return InvoiceView.serialize_invoice_with_details(invoice), 200
    
    @staticmethod
    def _calculate_totals(invoice):
        """Calculate invoice totals"""
        subtotal = sum(detail.line_total for detail in invoice.invoice_details)
        tax = sum(detail.line_total * detail.tax_percentage / 100 for detail in invoice.invoice_details)
        
        invoice.subtotal = subtotal
        invoice.tax_amount = tax
        invoice.total_amount = subtotal + tax


# Routes
@invoice_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    result, status = InvoiceController.create_invoice(data)
    return jsonify(result), status

@invoice_bp.route('/<int:invoice_id>', methods=['GET'])
def get_one(invoice_id):
    result, status = InvoiceController.get_invoice(invoice_id)
    return jsonify(result), status

@invoice_bp.route('/', methods=['GET'])
def get_all():
    result, status = InvoiceController.get_all_invoices()
    return jsonify(result), status

@invoice_bp.route('/<int:invoice_id>', methods=['PUT'])
def update(invoice_id):
    data = request.get_json()
    result, status = InvoiceController.update_invoice(invoice_id, data)
    return jsonify(result), status

@invoice_bp.route('/<int:invoice_id>', methods=['DELETE'])
def delete(invoice_id):
    result, status = InvoiceController.delete_invoice(invoice_id)
    return jsonify(result), status

@invoice_bp.route('/<int:invoice_id>/issue', methods=['PUT'])
def issue(invoice_id):
    result, status = InvoiceController.issue_invoice(invoice_id)
    return jsonify(result), status
