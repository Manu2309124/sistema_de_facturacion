from flask import Blueprint, request, jsonify
from app.database import db
from app.models.product import Product
from app.views.product_view import ProductView

product_bp = Blueprint('products', __name__)

class ProductController:
    """Business logic for products"""
    
    @staticmethod
    def create_product(data):
        """Create a new product"""
        product = Product(
            code=data.get('code'),
            name=data.get('name'),
            description=data.get('description'),
            price=data.get('price'),
            tax_percentage=data.get('tax_percentage', 0.0),
            stock=data.get('stock', 0)
        )
        
        db.session.add(product)
        db.session.commit()
        return ProductView.serialize_product(product), 201
    
    @staticmethod
    def get_product(product_id):
        """Get product by ID"""
        product = Product.query.get(product_id)
        if not product:
            return {'error': 'Product not found'}, 404
        return ProductView.serialize_product(product), 200
    
    @staticmethod
    def get_all_products():
        """Get all products"""
        products = Product.query.all()
        return ProductView.serialize_products(products), 200
    
    @staticmethod
    def update_product(product_id, data):
        """Update product"""
        product = Product.query.get(product_id)
        if not product:
            return {'error': 'Product not found'}, 404
        
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.tax_percentage = data.get('tax_percentage', product.tax_percentage)
        product.stock = data.get('stock', product.stock)
        
        db.session.commit()
        return ProductView.serialize_product(product), 200
    
    @staticmethod
    def delete_product(product_id):
        """Delete product"""
        product = Product.query.get(product_id)
        if not product:
            return {'error': 'Product not found'}, 404
        
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted'}, 200


# Routes
@product_bp.route('/', methods=['POST'])
def create():
    data = request.get_json()
    result, status = ProductController.create_product(data)
    return jsonify(result), status

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_one(product_id):
    result, status = ProductController.get_product(product_id)
    return jsonify(result), status

@product_bp.route('/', methods=['GET'])
def get_all():
    result, status = ProductController.get_all_products()
    return jsonify(result), status

@product_bp.route('/<int:product_id>', methods=['PUT'])
def update(product_id):
    data = request.get_json()
    result, status = ProductController.update_product(product_id, data)
    return jsonify(result), status

@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete(product_id):
    result, status = ProductController.delete_product(product_id)
    return jsonify(result), status
