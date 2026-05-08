import unittest
from app import create_app
from app.database import db
from app.models.customer import Customer
from app.models.product import Product
from app.models.invoice import Invoice

class TestModels(unittest.TestCase):
    """Test models"""
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_customer_creation(self):
        """Test customer model creation"""
        customer = Customer(
            name='John Doe',
            email='john@example.com',
            phone='1234567890'
        )
        db.session.add(customer)
        db.session.commit()
        
        assert Customer.query.count() == 1
        assert customer.name == 'John Doe'
    
    def test_product_creation(self):
        """Test product model creation"""
        product = Product(
            code='PROD001',
            name='Product 1',
            price=100.0,
            tax_percentage=5.0
        )
        db.session.add(product)
        db.session.commit()
        
        assert Product.query.count() == 1
        assert product.price == 100.0
    
    def test_invoice_creation(self):
        """Test invoice model creation"""
        customer = Customer(
            name='John Doe',
            email='john@example.com'
        )
        db.session.add(customer)
        db.session.commit()
        
        invoice = Invoice(
            invoice_number='INV001',
            customer_id=customer.id
        )
        db.session.add(invoice)
        db.session.commit()
        
        assert Invoice.query.count() == 1
        assert invoice.invoice_number == 'INV001'

if __name__ == '__main__':
    unittest.main()
