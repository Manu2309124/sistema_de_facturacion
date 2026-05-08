from app.database import db

class InvoiceDetail(db.Model):
    """Invoice detail model for billing system"""
    __tablename__ = 'invoice_details'
    
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    tax_percentage = db.Column(db.Float, default=0.0)
    line_total = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'id': self.id,
            'invoice_id': self.invoice_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'tax_percentage': self.tax_percentage,
            'line_total': self.line_total
        }
    
    def __repr__(self):
        return f'<InvoiceDetail Invoice:{self.invoice_id} Product:{self.product_id}>'
