from . import db
from datetime import datetime, timezone

class Favorite(db.Model):
    favorite_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    travel_id = db.Column(db.Integer, db.ForeignKey('travel.travel_id'))
    added_date = db.Column(db.String(10), nullable=False,
                         default=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    added_time = db.Column(db.String(5), nullable=False,
                         default=lambda: datetime.now(timezone.utc).strftime("%H-%M"))
    
    def toDic(self):
        return {
            "favorite_id": self.favorite_id,
            "user_id": self.user_id,
            "travel_id": self.travel_id,
            "added_date": self.added_date,  # YYYY-MM-DD format
            "added_time": self.added_time   # HH-MM format
        }