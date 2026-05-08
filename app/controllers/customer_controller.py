from flask import Blueprint, request, jsonify
from app.database import db
from app.models.customer import Customer
from app.views.customer_view import CustomerView

customer_bp = Blueprint('customers', __name__)

class CustomerController:
    """Business logic for customers"""
    
    @staticmethod
    def create_customer(data):
        """Create a new customer"""
        customer = Customer(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            city=data.get('city'),
            country=data.get('country'),
            tax_id=data.get('tax_id')
        )
        
        db.session.add(customer)
        db.session.commit()
        return CustomerView.serialize_customer(customer), 201
    
    @staticmethod
    def get_customer(customer_id):
        """Get customer by ID"""
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Customer not found'}, 404
        return CustomerView.serialize_customer(customer), 200
    
    @staticmethod
    def get_all_customers():
        """Get all customers"""
        customers = Customer.query.all()
        return CustomerView.serialize_customers(customers), 200
    
    @staticmethod
    def update_customer(customer_id, data):
        """Update customer"""
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Customer not found'}, 404
        
        customer.name = data.get('name', customer.name)
        customer.email = data.get('email', customer.email)
        customer.phone = data.get('phone', customer.phone)
        customer.address = data.get('address', customer.address)
        customer.city = data.get('city', customer.city)
        customer.country = data.get('country', customer.country)
        customer.tax_id = data.get('tax_id', customer.tax_id)
        
        db.session.commit()
        return CustomerView.serialize_customer(customer), 200
    
    @staticmethod
    def delete_customer(customer_id):
        """Delete customer"""
        customer = Customer.query.get(customer_id)
        if not customer:
            return {'error': 'Customer not found'}, 404
        
        db.session.delete(customer)
        db.session.commit()
        return {'message': 'Customer deleted'}, 200


# Routes
@customer_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    result, status = CustomerController.create_customer(data)
    return jsonify(result), status

@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_one(customer_id):
    result, status = CustomerController.get_customer(customer_id)
    return jsonify(result), status

@customer_bp.route('/', methods=['GET'])
def get_all():
    result, status = CustomerController.get_all_customers()
    return jsonify(result), status

@customer_bp.route('/<int:customer_id>', methods=['PUT'])
def update(customer_id):
    data = request.get_json()
    result, status = CustomerController.update_customer(customer_id, data)
    return jsonify(result), status

@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete(customer_id):
    result, status = CustomerController.delete_customer(customer_id)
    return jsonify(result), status
