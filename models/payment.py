from . import db
from datetime import datetime, timezone

class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id'), nullable=False)
    fee = db.Column(db.Float, default=0, nullable=False)
    date = db.Column(db.String(10), nullable=False, 
                  default=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    is_valid = db.Column(db.Boolean, nullable=False, default=True)
    
    payment_method = db.Column(db.Integer, default=0, nullable=False)# 0 => insite , 1 => poste , 2 => card
     
    def toDic(self):
        return {
            "payment_id": self.payment_id,
            "user_id": self.user_id,
            "order_id": self.order_id,
            "fee": self.fee,
            "date": self.date,  # Already in YYYY-MM-DD format
            "is_valid": self.is_valid,
            "payment_method": self.payment_method
        }