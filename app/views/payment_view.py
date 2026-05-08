"""Payment view serializers"""

class PaymentView:
    """Payment response view"""
    
    @staticmethod
    def serialize_payment(payment):
        """Serialize a single payment"""
        return payment.to_dict()
    
    @staticmethod
    def serialize_payments(payments):
        """Serialize multiple payments"""
        return [payment.to_dict() for payment in payments]
