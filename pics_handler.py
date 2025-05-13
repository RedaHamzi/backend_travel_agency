import os
from werkzeug.utils import secure_filename
from flask import request
from models import db

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_pfp(user,file):
    if allowed_file(file.filename):
        filename = secure_filename(f"{user.user_id}_{file.filename}")
        filepath = os.path.join('static/profile_pics', filename)
        file.save(filepath)
        if (user.img_url and user.img_url != "static/profile_pics/default_pic.png"):
            os.remove(user.img_url)
        user.img_url = filepath

def delete_pfp(user):
    if (user.img_url and user.img_url != "static/profile_pics/default_pic.png"):
        os.remove(user.img_url)
    user.img_url = "static/profile_pics/default_pic.png"
    db.session.commit()
    return {"message": "Profile picture deleted successfully"}


def upload_pfp2(travel,file):
    if allowed_file(file.filename):
        filename = secure_filename(f"{travel.travel_id}_{file.filename}")
        filepath = os.path.join('static/travel_pics', filename)
        file.save(filepath)
        if (travel.img_url and travel.img_url != "static/travel_pics/default_pic.png"):
            os.remove(travel.img_url)
        travel.img_url = filepath

def delete_pfp2(travel):
    if (travel.img_url and travel.img_url != "static/travel_pics/default_pic.png"):
        os.remove(travel.img_url)
    travel.img_url = "static/travel_pics/default_pic.png"
    db.session.commit()
    return {"message": "Travel picture deleted successfully", "status":200}


def upload_pfp3(accomodation,file):
    if allowed_file(file.filename):
        filename = secure_filename(f"{accomodation.accomodation_id}_{file.filename}")
        filepath = os.path.join('static/accomodation_pics', filename)
        file.save(filepath)
        if (accomodation.picture_url and accomodation.picture_url != "static/accomodation_pics/default_pic.png"):
            os.remove(accomodation.picture_url)
        accomodation.picture_url = filepath

def delete_pfp3(accomodation):
    if (accomodation.picture_url and accomodation.picture_url != "static/accomodation_pics/default_pic.png"):
        os.remove(accomodation.picture_url)
    accomodation.picture_url = "static/accomodation_pics/default_pic.png"
    db.session.commit()
    return {"message": "accomodation picture deleted successfully"}
