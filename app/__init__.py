from flask import Flask
from app.database import db

def create_app(config_name='development'):
    """Application factory function"""
    app = Flask(__name__)
    
    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    from app.controllers.invoice_controller import invoice_bp
    from app.controllers.customer_controller import customer_bp
    from app.controllers.product_controller import product_bp
    from app.controllers.payment_controller import payment_bp
    
    app.register_blueprint(invoice_bp, url_prefix='/api/invoices')
    app.register_blueprint(customer_bp, url_prefix='/api/customers')
    app.register_blueprint(product_bp, url_prefix='/api/products')
    app.register_blueprint(payment_bp, url_prefix='/api/payments')
    
    return app
