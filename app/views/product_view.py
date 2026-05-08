"""Product view serializers"""

class ProductView:
    """Product response view"""
    
    @staticmethod
    def serialize_product(product):
        """Serialize a single product"""
        return product.to_dict()
    
    @staticmethod
    def serialize_products(products):
        """Serialize multiple products"""
        return [product.to_dict() for product in products]
