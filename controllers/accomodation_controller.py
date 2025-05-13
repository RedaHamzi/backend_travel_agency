## /controllers/accomodation_controllers.py
from models.accomodation import Accomodation, db
from pics_handler import upload_pfp3, delete_pfp3

def create_accomodation(data, file):
    new_accomodation = Accomodation(
        accomodation_type=data.get('accomodation_type', 'Hotel'),
        accomodation_name=data.get('accomodation_name'),
        picture_url="static/accomodation_pics/default_pic.png",
        rating=data.get('rating', 0),
        description=data.get('description'),
        price_per_night=data.get('price_per_night', 0),
        location=data.get('location')
    ) 
    db.session.add(new_accomodation)
    db.session.commit()
    if file:
        upload_pfp3(new_accomodation, file)
        db.session
    return {"message": "Accomodation created successfully","status":201, "data": new_accomodation.toDic()}
#---------------------------------------------------------------------------------------------------------------------
# def filter_accomodations(data):
#     accomodations = Accomodation.query.filter_by(**data).all()
#     return {"message":"getting all accomodations","status":200,"data": [a.toDic() for a in accomodations]}

def filter_accomodations(data):
    query = Accomodation.query
    
    # Filter by accommodation type
    if 'accomodation_type' in data:
        types = data['accomodation_type'].split(',')
        query = query.filter(Accomodation.accomodation_type.in_(types))
    
    if 'accomodation_id' in data:
        
        query = query.filter(Accomodation.accomodation_id == int(data['accomodation_id']))
    
    # Filter by minimum rating
    if 'min_rating' in data:
        query = query.filter(Accomodation.rating >= float(data['min_rating']))
    
    # Filter by price range
    if 'min_price' in data:
        query = query.filter(Accomodation.price_per_night >= float(data['min_price']))
    if 'max_price' in data:
        query = query.filter(Accomodation.price_per_night <= float(data['max_price']))
    
    # Filter by location
    if 'location' in data:
        query = query.filter(Accomodation.location.ilike(f"%{data['location']}%"))
    
    # Filter by description presence
    if 'has_description' in data and data['has_description'].lower() == 'true':
        query = query.filter(Accomodation.description != '', Accomodation.description.isnot(None))
    
    results = query.all()
    return {
        "message": "Filtered accommodations",
        "status": 200,
        "data": [a.toDic() for a in results]
    }
#------------------------------------------------------------------------------------------------------------------------
def get_accomodation(id):
    accomodation = Accomodation.query.get(id)
    if not accomodation:
        return {"message": "Accomodation not found","status":404}
    return {"message":"getting accomodation","status":200,"data":accomodation.toDic()}
#-------------------------------------------------------------------------------------------------------------------------
def update_accomodation(id, data, file):
    accomodation = Accomodation.query.get(id)
    if not accomodation:
        return {"message": "Accomodation not found","status":404}
    
    fields_to_update = ["accomodation_type", "accomodation_name", "picture_url", "rating", "description", "price_per_night", "location"]

    for field in fields_to_update:
        if field in data:
            setattr(accomodation, field, data[field])
    if file:
        delete_pfp3(accomodation)
        upload_pfp3(accomodation, file)
    db.session.commit()
    return {"message": "Accomodation updated successfully","status":200, "data": accomodation.toDic()}
#---------------------------------------------------------------------------------------------------------------------------
def delete_accomodation(id):
    accomodation = Accomodation.query.get(id)
    
    if not accomodation:
        return {"message": "Accomodation not found","status":404}
    delete_pfp3(accomodation)
    db.session.delete(accomodation)
    db.session.commit()
    return {"message": "Accomodation deleted successfully","status":200}
