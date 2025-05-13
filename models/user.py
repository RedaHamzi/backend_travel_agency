#/models/user.py
from . import db
from datetime import datetime

class User(db.Model):
    user_id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(255),nullable=False)
    img_url = db.Column(db.String(200),nullable=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    gender = db.Column(db.String(10),nullable=True)
    birth_date = db.Column(db.Date,nullable=True)
    is_super_admin = db.Column(db.Boolean,default=False) ## there is only one and he can add other admins
    is_admin = db.Column(db.Boolean,default=False)## second degree can't add admins
    is_blocked = db.Column(db.Boolean,default=False)
    score = db.Column(db.Integer,default=0)## for fidelity
    wallet = db.Column(db.Integer,default=0)## Zohire idea
    country = db.Column(db.String(50),nullable=True)
    
    
    reviews = db.relationship('Review', backref='user', lazy='subquery')
    orders = db.relationship('Order', backref='user', lazy='subquery')
    payments = db.relationship('Payment', backref='user', lazy='subquery')
    favorites = db.relationship('Favorite', backref='user', lazy='subquery')
    
     
    
    
    def toDic(self):
        return {
            "user_id" : self.user_id,
            "img_url" : self.img_url,
            "first_name" : self.first_name,
            "last_name" : self.last_name,
            "password" :  self.password,
            "email" : self.email,
            "gender" : self.gender,
            "birth_date": self.birth_date.strftime('%Y-%m-%d') if self.birth_date else None,
            "is_super_admin" : self.is_super_admin,
            "is_admin" : self.is_admin,
            "is_blocked" : self.is_blocked,
            "score" : self.score,
            "wallet" : self.wallet,
            "country" : self.country,
            
            "reviews": [review.toDic() for review in self.reviews] if self.reviews else [],
            "orders": [order.toDic() for order in self.orders] if self.orders else [],
            "payments": [payment.toDic() for payment in self.payments] if self.payments else [],
            "favorites": [favorite.toDic() for favorite in self.favorites] if self.favorites else []
        }