from . import db

class Accomodation(db.Model):
    accomodation_id = db.Column(db.Integer,primary_key = True)
    accomodation_type = db.Column(db.String(50),nullable=False,default="Hotel")
    accomodation_name = db.Column(db.String(50),nullable=True)
    picture_url = db.Column(db.String(255),nullable=True)
    rating = db.Column(db.Float,nullable=False,default=0)
    description = db.Column(db.Text,nullable=False)
    price_per_night = db.Column(db.Float,nullable=False,default=0)
    location = db.Column(db.String(100),nullable=False)
    
    def toDic(self):
        return {
            "accomodation_id" : self.accomodation_id,
            "accomodation_type" : self.accomodation_type,
            "accomodation_name" : self.accomodation_name,
            "picture_url" : self.picture_url,
            "rating" : self.rating,
            "description" : self.description,
            "price_per_night" : self.price_per_night,
            "location" : self.location
        }