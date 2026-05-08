"""Customer view serializers"""

class CustomerView:
    """Customer response view"""
    
    @staticmethod
    def serialize_customer(customer):
        """Serialize a single customer"""
        return customer.to_dict()
    
    @staticmethod
    def serialize_customers(customers):
        """Serialize multiple customers"""
        return [customer.to_dict() for customer in customers]
