"""Invoice view serializers"""

class InvoiceView:
    """Invoice response view"""
    
    @staticmethod
    def serialize_invoice(invoice):
        """Serialize a single invoice"""
        return invoice.to_dict()
    
    @staticmethod
    def serialize_invoices(invoices):
        """Serialize multiple invoices"""
        return [invoice.to_dict() for invoice in invoices]
    
    @staticmethod
    def serialize_invoice_with_details(invoice):
        """Serialize invoice with details"""
        data = invoice.to_dict()
        data['details'] = [detail.to_dict() for detail in invoice.invoice_details]
        data['payments'] = [payment.to_dict() for payment in invoice.payments]
        return data
