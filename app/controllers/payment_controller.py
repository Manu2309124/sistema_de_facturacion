from flask import Blueprint, request, jsonify
from app.database import db
from app.models.payment import Payment
from app.models.invoice import Invoice
from app.views.payment_view import PaymentView

payment_bp = Blueprint('payments', __name__)

class PaymentController:
    """Business logic for payments"""
    
    @staticmethod
    def create_payment(data):
        """Create a new payment"""
        invoice = Invoice.query.get(data.get('invoice_id'))
        if not invoice:
            return {'error': 'Invoice not found'}, 404
        
        payment = Payment(
            invoice_id=data.get('invoice_id'),
            amount=data.get('amount'),
            payment_method=data.get('payment_method'),
            reference=data.get('reference'),
            notes=data.get('notes')
        )
        
        db.session.add(payment)
        
        # Check if invoice is fully paid
        total_paid = sum(p.amount for p in invoice.payments) + payment.amount
        if total_paid >= invoice.total_amount:
            invoice.status = 'paid'
        
        db.session.commit()
        return PaymentView.serialize_payment(payment), 201
    
    @staticmethod
    def get_payment(payment_id):
        """Get payment by ID"""
        payment = Payment.query.get(payment_id)
        if not payment:
            return {'error': 'Payment not found'}, 404
        return PaymentView.serialize_payment(payment), 200
    
    @staticmethod
    def get_invoice_payments(invoice_id):
        """Get all payments for an invoice"""
        invoice = Invoice.query.get(invoice_id)
        if not invoice:
            return {'error': 'Invoice not found'}, 404
        
        payments = Payment.query.filter_by(invoice_id=invoice_id).all()
        return PaymentView.serialize_payments(payments), 200
    
    @staticmethod
    def delete_payment(payment_id):
        """Delete payment"""
        payment = Payment.query.get(payment_id)
        if not payment:
            return {'error': 'Payment not found'}, 404
        
        invoice = Invoice.query.get(payment.invoice_id)
        db.session.delete(payment)
        
        # Revert invoice status if needed
        total_paid = sum(p.amount for p in invoice.payments if p.id != payment_id)
        if total_paid < invoice.total_amount and invoice.status == 'paid':
            invoice.status = 'issued'
        
        db.session.commit()
        return {'message': 'Payment deleted'}, 200


# Routes
@payment_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    result, status = PaymentController.create_payment(data)
    return jsonify(result), status

@payment_bp.route('/<int:payment_id>', methods=['GET'])
def get_one(payment_id):
    result, status = PaymentController.get_payment(payment_id)
    return jsonify(result), status

@payment_bp.route('/invoice/<int:invoice_id>', methods=['GET'])
def get_invoice_payments(invoice_id):
    result, status = PaymentController.get_invoice_payments(invoice_id)
    return jsonify(result), status

@payment_bp.route('/<int:payment_id>', methods=['DELETE'])
def delete(payment_id):
    result, status = PaymentController.delete_payment(payment_id)
    return jsonify(result), status
