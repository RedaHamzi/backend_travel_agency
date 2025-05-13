from . import db 
from datetime import datetime, timezone

class Ticket(db.Model):
    ticket_id = db.Column(db.Integer, primary_key=True)
    travel_id = db.Column(db.Integer, db.ForeignKey("travel.travel_id"), nullable=True)
    price_for_one = db.Column(db.Float, nullable=False, default=0)
    transportation_organization = db.Column(db.String(100), nullable=False)  # e.g., air algerie or air france
    date = db.Column(db.String(10), nullable=False, default=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    time = db.Column(db.String(5), nullable=False, default=lambda: datetime.now(timezone.utc).strftime("%H-%M"))
    date_comback = db.Column(db.String(10), nullable=False, default=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    time_comback = db.Column(db.String(5), nullable=False, default=lambda: datetime.now(timezone.utc).strftime("%H-%M"))
    starting_place = db.Column(db.String(150), nullable=False)  # country, city, station
    destination_place = db.Column(db.String(150), nullable=False)
    travel_method = db.Column(db.String(100), nullable=False)  # plane, ship, bus, car
    starting_place_comeback = db.Column(db.String(150), nullable=False)
    destination_place_comeback = db.Column(db.String(150), nullable=False)
    have_stopover = db.Column(db.Boolean, default=False)  # stopover/escale
    
    def toDic(self):
        return {
            "ticket_id": self.ticket_id,
            "travel_id": self.travel_id,
            "price_for_one": self.price_for_one,
            "transportation_organization": self.transportation_organization,
            "date": self.date,  # Already in YYYY-MM-DD format
            "time": self.time,  # Already in HH-MM format
            "date_comback": self.date_comback,  # Already in YYYY-MM-DD format
            "time_comback": self.time_comback,  # Already in HH-MM format
            "starting_place": self.starting_place,
            "destination_place": self.destination_place,
            "travel_method": self.travel_method,
            "starting_place_comeback": self.starting_place_comeback,
            "destination_place_comeback": self.destination_place_comeback,
            "have_stopover": self.have_stopover
        }