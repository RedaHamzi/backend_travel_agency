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
import re
from datetime import datetime, timezone




def string_to_date(date_string, format="%Y-%m-%d"):
    try:
        return datetime.strptime(date_string, format).date()
    except ValueError:
        return None



def string_to_time(time_string, format="%H:%M"):
    try:
        return datetime.strptime(time_string, format).time()
    except ValueError:
        return None  


fields = [
        "ticket_id","price_for_one", "transportation_organization",
        "date", "date_comback", "starting_place",
        "destination_place", "travel_method", "starting_place_comeback",
        "destination_place_comeback", "have_stopover","time","time_comback"
    ]



def add_ticket(data):
    required_fields = [
        "travel_id", "price_for_one",
        "transportation_organization", "date", "date_comback",
        "starting_place", "destination_place",
        "travel_method", "starting_place_comeback",
        "destination_place_comeback", "time", "time_comback"
    ]
    for field in required_fields:
        field_value = data.get(field)  
        if field_value is None:
            return {"message": f"{field} is required", "status":400}
        if field == 'date' or field == 'date_comback':
            field_value = string_to_date(field_value)
            if field_value is None:
                return {"message": f"Invalid date format for {field}","status":400}
        elif field == 'time' or field == 'time_comback':
            field_value = string_to_time(field_value)
            if field_value is None:
                return {"message": f"Invalid time format for {field}","status":400}
    ticket = Ticket(
        travel_id = data['travel_id'],
        price_for_one = data['price_for_one'],
        transportation_organization = data['transportation_organization'],
        date = string_to_date(data['date']),
        time = data['time'],
        date_comback = string_to_date(data['date_comback']),
        time_comback = data.get('time_comback'),
        starting_place = data['starting_place'],
        destination_place = data['destination_place'],
        travel_method = data['travel_method'],
        starting_place_comeback = data['starting_place_comeback'],
        destination_place_comeback = data['destination_place_comeback'],
        have_stopover = data.get('have_stopover',False) 

    )
    db.session.add(ticket)
    db.session.commit()
    return {"message": "Ticket added successfully", "status":200, "data":ticket.toDic()}



def get_tickets_by_filter(data):
    
    # Checkin  for invalid fields
    for field in data:
        if field not in fields:
            return {"message": f"Invalid field {field}","status":400}
    
    # Applying filters dynamically
    tickets = Ticket.query.filter_by(**data).all()
    
    if not tickets:
        return {"message": "No ticket found with this filter","status":404}
    else:
        return {"message":"Filter done successfully", "status":200,"data":[ticket.toDic() for ticket in tickets]}






def update_ticket(data,id):
    ticket = Ticket.query.get(id)
    if ticket is None:
        return {"message": "Ticket not found","status":404}   

    for field in fields:
        
        field_value = data.get(field)

        if field_value is not None:
            if field == 'date' or field == 'date_comback':
                field_value = string_to_date(field_value)
                if field_value is None:
                    return {"message": f"Invalid date format for {field}","status":400}
                setattr(ticket, field, field_value)
            elif field == 'time' or field == 'time_comback':
                field_value = string_to_time(field_value)
                if field_value is None:
                    return {"message": f"Invalid time format for {field}","status":400}
                setattr(ticket, field, data.get(field))
            else:
                
                setattr(ticket, field, field_value)



            
        
    db.session.commit()
    return {"message": "Ticket updated successfully","status":200,"data":ticket.toDic()}





def delete_ticket(id):
    if id is None:
        return {"message": "Ticket id is required","status":400}
    ticket = Ticket.query.get(id)
    if ticket is None:
        return {"message": "Ticket not found","status":404}
    db.session.delete(ticket)
    db.session.commit()
    return {"message": "Ticket deleted successfully","status":200}
    
