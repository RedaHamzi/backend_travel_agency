# /controllers/travel_controller
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
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from flask_jwt_extended import create_access_token, get_jwt_identity
from CodeConfirmation import send_confirmation_code
from datetime import datetime, timezone
from secure_password import is_secure_password
import re
from pics_handler import upload_pfp2, delete_pfp2


def create_travel(data, file):
    required_fields = ['destination_country', 'duration', 'price', 'destination_city', 'accomodation_id']
    for field in required_fields:
        if field not in data:
            return {'message': f'{field} is required', 'status': 400}
    
    travel = Travel(
        destination_country = data['destination_country'],
        destination_city = data['destination_city'],
        duration = data['duration'],
        price = data['price'],
        img_url = "static/travel_pics/default_pic.png",
        accomodation_id = data['accomodation_id'],
        have_organized = data.get('have_organized', False),
        have_guide = data.get('have_guide', False),
        is_desp = data.get('is_desp', True),
        description = data.get('description', None)
    )

    db.session.add(travel)
    db.session.commit()
    if file:
        upload_pfp2(travel,file)
        db.session.commit()
    return {'message': 'Travel created successfully', 'status': 201,"data": travel.toDic()}


def update_travel_(data,file, id):
    travel = Travel.query.filter_by(travel_id=id).first()
    if travel is None:
        return {"message": "Travel not found", "status": 404}
    
    fields_that_can_be_updated = ["have_guide", "have_organized", "is_desp", "description" ,'destination_country', 'duration', 'price', 'destination_city', 'accomodation_id']
    if data:
        for field in fields_that_can_be_updated:
            field_value = data.get(field)
            if field_value is not None:
                setattr(travel, field, field_value) 
    if file:
        delete_pfp2(travel)
        upload_pfp2(travel,file)  
    db.session.commit()  
        
    return {"message": "Travel updated successfully", "status": 200,"data": travel.toDic()}

    

def filter_travels(data):
    destination_country = data.get('destination_country')
    destination_city = data.get('destination_city')
    min_price = data.get('min_price')
    max_price = data.get('max_price')
    available_only = data.get('available_only')
    not_available_only = data.get('not_available_only')
    travel_id = data.get('travel_id')

    query = Travel.query

    if destination_country:
        query = query.filter(Travel.destination_country.ilike(f"%{destination_country}%"))
    if destination_city:
        query = query.filter(Travel.destination_city.ilike(f"%{destination_city}%"))
    if min_price is not None:
        query = query.filter(Travel.price >= min_price)
    if max_price is not None:
        query = query.filter(Travel.price <= max_price)
    if travel_id is not None:
        query = query.filter(Travel.travel_id == travel_id)

    # Handle available and not available flags correctly
    if available_only is True:
        query = query.filter(Travel.is_desp == True)
    elif not_available_only is True:
        query = query.filter(Travel.is_desp == False)

    travels = query.all()
    return {"message" : "Success", "status": 200, "data": [travel.toDic() for travel in travels]}


def remove_travel(id):
    travel = Travel.query.filter_by(travel_id = id).first()
    delete_pfp2(travel)
    db.session.delete(travel)
    db.session.commit()
    return {"message": "Travel removed successfully", "status": 200}
