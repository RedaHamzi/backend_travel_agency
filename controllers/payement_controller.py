from flask_jwt_extended import get_jwt_identity
from models.payment import Payment, db
from models.order import Order

def get_payments_by_filter(filters):
    """
    Get payments based on filters
    Filters can include:
    - user_id (int)
    - order_id (int)
    - start_date (date string in YYYY-MM-DD format)
    - end_date (date string in YYYY-MM-DD format)
    - is_valid (bool)
    """
    query = Payment.query
    
    if 'user_id' in filters:
        query = query.filter_by(user_id=filters['user_id'])
    
    if 'order_id' in filters:
        query = query.filter_by(order_id=filters['order_id'])
    
    if 'is_valid' in filters:
        query = query.filter_by(is_valid=filters['is_valid'])
    
    if 'start_date' in filters:
        query = query.filter(Payment.date >= filters['start_date'])
    
    if 'end_date' in filters:
        query = query.filter(Payment.date <= filters['end_date'])
    
    payments = query.all()
    return {
        "message": "Payments retrieved successfully",
        "status": 200,
        "data": [payment.toDic() for payment in payments]
    }

 
def create_payment(data):
    id = get_jwt_identity()
    new_payment = Payment(
        user_id=id,
        order_id=data['order_id'],
        fee=(Order.query.filter_by(order_id = data["order_id"]).first()).price,
        is_valid=False
    )
    db.session.add(new_payment) 
    db.session.commit()
    return {"message": "Payment created successfully!","status":201, "data": new_payment.toDic()}

# this one is for onsite and with "mandat" payments
def create_payment1(data):
    new_payment = Payment(
        user_id=data['user_id'], 
        order_id=data['order_id'],
        fee=(Order.query.filter_by(order_id = data["order_id"]).first()).price,
        is_valid=True,
        payment_method=data["payment_method"]
    )
    db.session.add(new_payment)
    db.session.commit()
    return {"message": "Payment created successfully!","status":201, "data": new_payment.toDic()}
 
def get_all_payments():
    payments = Payment.query.all()
    return {"message":"getting all payments","status":200,"data":[payment.toDic() for payment in payments]}

def get_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if payment is None:
        return {"message": "Payment not found","status":404}
    return {"message":"getting payment","status":200,"data":payment.toDic()}

def update_payment(payment_id, data):
    # u can use this to validate a payment
    payment = Payment.query.get(payment_id)
    if payment is None:
        return {"message": "Payment not found","status":404}

    payment.amount = data.get("amount", payment.amount)
    payment.payment_date = data.get("payment_date", payment.payment_date)
    payment.status = data.get("status", payment.status)

    db.session.commit()
    return {"message": "Payment updated successfully!","status":200, "data": payment.toDic()}

 
def delete_payment(payment_id):
    payment = Payment.query.filter_by(payment_id).first()
    if payment is None:
        return {"message": "Payment not found","status":404}

    payment.is_valid = False
    db.session.commit()
    return {"message": "Payment deleted successfully!", "status":200, "data":payment.toDic()}

def validate_payment(id):
    payment = Payment.query.filter_by(payment_id=id).first()
    payment.is_valid = True
    return {"message": "Payment validated successfully!", "status":200, "data":payment.toDic()}
