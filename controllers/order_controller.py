#/controllers/order_controller.py
import random
import string
from models.user import User
from models.favorite import Favorite
from models.accomodation import Accomodation
from models.order import Order
from models.review import Review
from models.ticket import Ticket
from models.travel import Travel
from models.payment import Payment
from models import db 
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
import datetime



from datetime import datetime, timezone

def string_to_date(date_string, format="%Y-%m-%d"):
    try:
        return datetime.strptime(date_string, format).date()
    except ValueError: 
        return None
    
def calculate_price(ticket, number, travel, id, org, guide):
    number = int(number)
    accomodation = Accomodation.query.filter_by(accomodation_id=travel.accomodation_id).first()
    user = User.query.filter_by(user_id=id).first()
    price = (ticket.price_for_one  + travel.price + accomodation.price_per_night*travel.duration) * number
    
    # guide and organization
    if guide and org:
        price += price*0.225
    elif guide or org:
        price += price*0.15

    # score
    if user.score > 0:
        if user.score > 100:
            price/=2
        else :
            price -= user.score/2*price/100
    
    # wallet
    if user.wallet > 0:
        if user.wallet > price:
            user.wallet -=price
            price = 0
        else :
            price -= user.wallet
            user.wallet = 0
    return price
    

def add_order(data):
    REQUIRED_FIELDS = ["travel_id", "ticket_id", "number"]
    for field in REQUIRED_FIELDS:
        field_value = data.get(field)
        if not field_value:
            return {"message": f"The {field} field is required", "status": 400}
    if not data.get("is_organized"):
        data["is_organized"] = False
    if not data.get("with_guide"):
        data["with_guide"] = False
    if not data.get("added_date"):
        data["added_date"] = datetime.now(timezone.utc).date()
    if not data.get("is_blocked"):
        data["is_blocked"] = False
    travel = Travel.query.filter_by(travel_id = data["travel_id"]).first()
    if travel.is_desp == False:
        return {"message": "This travel is not available", "status": 400}
    if travel.have_organized == False and data["is_organized"] == True :
        return {"message": "This travel is not available with organization", "status": 400}
    if travel.have_guide == False and data["with_guide"] == True :
        return {"message": "This travel is not available with guide", "status": 400}
    ticket = Ticket.query.get(data["ticket_id"])
    new_order = Order(
        travel_id=data["travel_id"],
        ticket_id=data["ticket_id"],
        user_id=int(get_jwt_identity()),
        number=data["number"],
        price=calculate_price(ticket, data["number"], travel, int(get_jwt_identity()), data["is_organized"], data["with_guide"]),
        is_organized=data.get("is_organized", False),
        with_guide=data.get("with_guide", False),
        added_date=data.get("added_date"),
        is_blocked=data.get("is_blocked", False)
    )    
    db.session.add(new_order)
    db.session.commit()
    return {"message": "Order added successfully", "status": 201, "data": new_order.toDic()}
 

def cancel_order(order_id):
   
    order = Order.query.filter_by(order_id = order_id).first()
    if not order:
        return {"message": "Order not found", "status": 404}
    if order.user_id != int(get_jwt_identity()):
        return {"message": "Unauthorized", "status": 401}

    order.is_blocked = True
    payment = Payment.query.filter_by(user_id=int(get_jwt_identity()), order_id = order_id).first()
    payment.is_valid = False
    user = User.query.filter_by(user_id = payment.user_id).first()
    t=payment.fee*0.1
    f=payment.fee*0.9
    user.wallet += t
    db.session.commit()
    return {"message": f"Order deleted successfully, {t}dz added to your wallet, {f}dz  back to your account", "status": 200}   



def get_order_by_filter(data):
    fields = ["order_id","travel_id", "ticket_id", "number", "price", "is_organized", "with_guide", "added_date", "is_blocked"]
    user = User.query.filter_by(user_id=int(get_jwt_identity())).first()
    if (user.is_admin == True or user.is_super_admin == True):
        fields.append("user_id")
    for field in data:
        if field not in fields:
            return {"message" : f"Invalid field {field}", "status": 400}
    orders = Order.query.filter_by(**data).all()
    if not orders:
        return {"message" : "No order found with this filter", "status": 404}
    else :
        return {"message":"getting orders by filter","status":200,"data":[order.toDic() for order in orders]}




def update_order(data, order_id):
    order = Order.query.get(order_id)
    curr = User.query.filter_by(user_id = int(get_jwt_identity())).first()
    if not order:
        return {"message": "Order not found","status":404}
    
    if not curr.is_admin and not curr.is_super_admin and order.user_id != curr.user_id:
        return {"message": "Unauthorized","status":401}
    
    fields = ["travel_id", "ticket_id", "number", "price", "is_organized", 
             "with_guide", "is_blocked", "added_date"]  # Added missing field
    
    for field in data:
        if field not in fields:
            return {"message": f"Invalid field {field}","status" : 400}

    try:
        for field in fields:
            if field in data:
                field_value = data[field]
                if field == 'added_date' and field_value is not None:
                    field_value = string_to_date(field_value)
                    if field_value is None:
                        return {"message": f"Invalid date format for {field}","status":400}
                setattr(order, field, field_value)
        
        db.session.commit()
        return {"message": "Order updated successfully", "data": order.toDic(),"status":200}
    except Exception as e:
        db.session.rollback()
        return {"message": f"Error updating order: {str(e)}","status":500}