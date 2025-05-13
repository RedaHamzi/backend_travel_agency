from . import db
from datetime import datetime, timezone

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    travel_id = db.Column(db.Integer, db.ForeignKey('travel.travel_id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.ticket_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    number = db.Column(db.Integer, default=1)
    price = db.Column(db.Float, nullable=False)
    is_organized = db.Column(db.Boolean, default=False)
    with_guide = db.Column(db.Boolean, default=False)
    added_date = db.Column(db.String(10), nullable=False,
                         default=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    is_blocked = db.Column(db.Boolean, default=False)
    
    payments = db.relationship('Payment', backref='order', lazy="subquery")

    def toDic(self):
        return {
            "order_id": self.order_id,
            "travel_id": self.travel_id,
            "travel": {
                "travel_id": self.travel.travel_id,
                "destination_country": self.travel.destination_country,
                "destination_city": self.travel.destination_city,
                "price": self.travel.price,
                "img_url": self.travel.img_url
            } if self.travel else None, 
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "number": self.number,
            "price": self.price,
            "is_organized": self.is_organized,
            "with_guide": self.with_guide,
            "added_date": self.added_date,  # Now in YYYY-MM-DD string format
            "is_blocked": self.is_blocked,
            "payments": [payment.toDic() for payment in self.payments] if self.payments else [],
        }