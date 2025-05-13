from . import db
from datetime import datetime, timezone

class Review(db.Model):
    review_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    travel_id = db.Column(db.Integer, db.ForeignKey('travel.travel_id'))
    date = db.Column(db.String(10), nullable=False, 
                  default=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"))
    time = db.Column(db.String(5), nullable=False,
                  default=lambda: datetime.now(timezone.utc).strftime("%H-%M"))
    
    def toDic(self):
        return {
            "review_id": self.review_id,
            "title": self.title,
            "rating": self.rating,
            "content": self.content,
            "user_id": self.user_id,
            "travel_id": self.travel_id,
            "date": self.date,  # Already in YYYY-MM-DD format
            "time": self.time   # Already in HH-MM format
        }