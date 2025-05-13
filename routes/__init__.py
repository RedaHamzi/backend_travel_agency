from .userRoutes import user_bp
from .reviewRoutes import review_bp
from .ticketRoutes import ticket_bp
from .travelRoutes import travel_bp
from .paymentRoutes import payment_bp
from .orderRoutes import order_bp
from .favoriteRoutes import favorite_bp
from .accomodationRoutes import accomodation_bp



def initialize_routes(app):
    app.register_blueprint(user_bp,url_prefix='/api/user')
    app.register_blueprint(review_bp,url_prefix='/api/review')
    app.register_blueprint(ticket_bp,url_prefix='/api/ticket')
    app.register_blueprint(travel_bp,url_prefix='/api/travel')
    app.register_blueprint(payment_bp,url_prefix='/api/payment')
    app.register_blueprint(order_bp,url_prefix='/api/order')
    app.register_blueprint(favorite_bp,url_prefix='/api/favorite')
    app.register_blueprint(accomodation_bp,url_prefix='/api/accomodation')
    
    