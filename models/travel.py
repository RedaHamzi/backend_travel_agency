from . import db
from datetime import datetime, timezone

class Travel(db.Model):
    travel_id = db.Column(db.Integer, primary_key=True)
    destination_country = db.Column(db.String(100), nullable=False)
    destination_city = db.Column(db.String(100), nullable=True)
    have_organized = db.Column(db.Boolean, default=False)
    have_guide = db.Column(db.Boolean, default=False)
    is_desp = db.Column(db.Boolean, default=True)  # disponible
    description = db.Column(db.String(200), nullable=True)
    accomodation_id = db.Column(db.Integer, db.ForeignKey('accomodation.accomodation_id'))
    duration = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String(200), nullable=False)
    
    # New date/time fields
    created_date = db.Column(db.String(10), nullable=False, 
                           default=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    created_time = db.Column(db.String(5), nullable=False,
                           default=lambda: datetime.now(timezone.utc).strftime("%H-%M"))
    last_updated_date = db.Column(db.String(10), nullable=False,
                                default=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                                onupdate=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    last_updated_time = db.Column(db.String(5), nullable=False,
                                default=lambda: datetime.now(timezone.utc).strftime("%H-%M"),
                                onupdate=lambda: datetime.now(timezone.utc).strftime("%H-%M"))
    
    reviews = db.relationship('Review', backref='travel', lazy="subquery")
    tickets = db.relationship('Ticket', backref='travel', lazy="subquery")
    orders = db.relationship('Order', backref='travel', lazy="subquery")
    
    def toDic(self):
        return {
            "travel_id": self.travel_id,
            "destination_country": self.destination_country,
            "destination_city": self.destination_city,
            "have_organized": self.have_organized,
            "have_guide": self.have_guide,
            "is_desp": self.is_desp,
            "description": self.description,
            "accomodation_id": self.accomodation_id,    
            "duration": self.duration,
            "price": self.price,
            "img_url": self.img_url,
            "created_date": self.created_date,
            "created_time": self.created_time,
            "last_updated_date": self.last_updated_date,
            "last_updated_time": self.last_updated_time,
            "reviews": [review.toDic() for review in self.reviews] if self.reviews else [],
            "tickets": [ticket.toDic() for ticket in self.tickets] if self.tickets else [],
            "orders": [order.toDic() for order in self.orders] if self.orders else [],
        }