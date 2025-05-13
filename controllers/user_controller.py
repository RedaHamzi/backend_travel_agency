## /controllers/user_controller.py
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
from flask import jsonify, request,current_app
from werkzeug.security import generate_password_hash, check_password_hash
# import jwt
from flask_jwt_extended import create_access_token, get_jwt_identity
from CodeConfirmation import send_confirmation_code
from datetime import datetime,timezone
from secure_password import is_secure_password
import re
from pics_handler import upload_pfp
from datetime import datetime




def is_valid_email(email):
    # This regex checks for a simple email format:
    # - Begins with one or more alphanumeric characters (including ., _, %, +, and -)
    # - Contains an '@' symbol
    # - Followed by a domain name with one or more alphanumeric characters or hyphens
    # - Ends with a dot and at least two alphabetic characters (e.g., .com, .org)
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def create_token(id):
    user = User.query.filter_by(user_id = id).first()
    access_token = create_access_token(identity=str(id),additional_claims=user.toDic())
    return access_token

l=["123456", 1]

def create_user_1(data):#client
    # Check if all required fields are present
    required_fields = ['last_name', 'first_name' , 'gender', 'email', 'password']
    if not all(field in data for field in required_fields):
        return {"message": "Missing required fields", "status": 400}
    # check for valid mail
    if not is_valid_email(data['email']):
        return {"message": "Invalid email", "status": 400}
    # Check if email already exists
    if User.query.filter_by(email=data['email']).first() is not None:
        return {"message": "Email already exist", "status": 400}
    l[0], l[1] = (send_confirmation_code(data['email']))
    return {"message": "Code sent", "status": 200}

def create_user_2(data):#client
    # Check the confirmation code
    if data.get('code') is None:
        return {"message": "Missing confirmation code", "status": 400}
    elif data['code'] != l[0]:
        return {"message": "Invalid confirmation code", "status": 400}
    elif l[1] < datetime.now(timezone.utc):
        return {"message": "Verification code expired", "status": 400}
    birthdate_str = data.get('birth_date')
    birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d') if birthdate_str else None
    # Create a new user
    new_user = User(
        last_name=data['last_name'],
        first_name=data['first_name'],
        password = generate_password_hash(data['password']),
        email=data.get('email',None),
        gender=data.get('gender',None),
        birth_date =  birthdate,
        is_admin=data.get('is_admin', False),
        is_blocked=data.get('is_blocked', False),
        score = data.get('score'),
        wallet = data.get('wallet'),
        country = data.get('country'),
        img_url = "static/profile_pics/default_pic.png"
    )
        
    # Add user to the database
    db.session.add(new_user)
    db.session.commit()

    return {'message': 'User created successfully','status': 201, 'user_id': new_user.user_id}

  
def login(data):
    # Check if all required fields are present
    required_fields = ['email', 'password']
    if not all(field in data for field in required_fields):
        return {'message': 'Missing required fields',"status":400}

    # Check if user exists
    user = User.query.filter_by(email=data['email']).first()
    if user is None:
        return {'message': 'User not found',"status":400}

    # Check if password is correct
    elif not check_password_hash(user.password,data.get('password')):
        return {'message': 'Invalid password',"status":400}
    elif user.is_blocked:
        return {'message': 'Your account has been blocked. Contact support for assistance.',"status":400}

    # Create JWT tokens
    else :
        access_token = create_token(user.user_id)
        return {"message" : "success","status":200,"data" : user.toDic(),'access_token': access_token} 

    
def get_user(id):
    curr = User.query.filter_by(user_id = id).first()
    if not curr:
        return {"message" : f"No user with id: {id}","status":404}
    else :
        return {"message" : "success","status":200,"data" : curr.toDic()}


def remove_admin(id):
    curr=User.query.filter_by(user_id = id).first()
    curr.is_admin = False
    db.session.commit()
    return {"message" : "Admin removed successfully","status":200}
    

def get_user_by_filter(data):
    fields = ['last_name', 'first_name' , 'gender', 'email', 'password', "country", "is_blocked", "score", "wallet", "birth_date", "user_id"]
    for field in data:
        if field not in fields:
            return {"message" : f"Invalid field {field}","status":400}
    users = User.query.filter_by(**data,is_super_admin=False).all()
    if not users:
        return {"message" : "No user found with this filter","status":404}
    else :
        return {"message" : "success","status":200,"data" : [user.toDic() for user in users]}


def forgot_password_enter_email_(data):
   
    email = data.get('email') 
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"message": "User not found","status":404}
    else:
        l[0], l[1] = send_confirmation_code(data['email'])
                                
        return {"message": "Verification code sent to email","status":200}
    


def forgot_password_verify_code_(data):
    email = data.get('email')
    reset_code = data.get('reset_code')
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"message": "User not found","status":404}
    if l[0] != reset_code:
        return {"message": "Invalid verification code","status":400}
    if  l[1] < datetime.now(timezone.utc):
        return {"message": "Verification code expired","status":400}

    return {"message": "Verification code verified","status":200}
    
    
    
def forgot_password_reset_password_(data):
    email = data.get('email')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    user = User.query.filter_by(email=email).first()
    if not user: 
        return {"message": "User not found","status":404}
    
    #Check if the new password and confirm password match
    if new_password != confirm_password:
        return {"message": "Passwords do not match","status":400}
    
    # Check if the new password is secure
    is_secure, message = is_secure_password(new_password)
    if not is_secure:
        return {"message": message,"status":400}
    

    user.password = generate_password_hash(new_password)
    user.reset_code = None
    user.reset_attempts = 0
    user.reset_expiry = None
    db.session.commit()
    return {"message": "Password reset successfully","status":200}


#####forgot password





def update_user_(data, file, id):
    user = User.query.filter_by(user_id=id).first()
    if user is None:
        return {"message": "User not found", "status": 404}

    # Update general fields
    fields_that_can_be_updated = ['first_name', 'last_name', 'gender', 'birth_date', 'country']
    if data:
        for field in fields_that_can_be_updated:
            field_value = data.get(field)
            if field_value is not None:
                if field == "birth_date":
                    try:
                        field_value = datetime.strptime(field_value, "%Y-%m-%d").date()
                    except ValueError:
                        return {"message": "Invalid date format for birth_date. Use YYYY-MM-DD.", "status": 400}
                setattr(user, field, field_value)

    # Handle profile picture
    if file:
        upload_pfp(user, file)

    # Handle password update
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    if current_password and new_password:
        if not check_password_hash(user.password, current_password):
            return {"message": "Current password is incorrect", "status": 401}
        if not is_secure_password(new_password):
            return {"message": "New password is not secure", "status": 400}
        user.password = generate_password_hash(new_password)

    db.session.commit()

    return {"message": "User updated successfully", "status": 200, "data": user.toDic()}

def create_super_admin():
    try:
        # Check if a super admin already exists
        existing_admin = User.query.filter_by(is_super_admin=True).first()
        if existing_admin:
            return {"message": "Super admin already exists", "status": 400}
        
        hashed_password = generate_password_hash("securepassword123")# Change this to your desired password (the inside of geenerate_password_hash)
        # Create a new super admin user
        super_admin = User(
            first_name="Admin",
            last_name="User",
            email="admin@example.com",  # Change this to your desired email
            password = hashed_password,  
            is_super_admin=True,
            is_admin=True
        )

        # Add to database session
        db.session.add(super_admin)
        db.session.commit()  # Commit changes

        return {"message": "Super admin created successfully!","status":201}

    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return {"message": str(e),"status":500}

def create_admin():
    data = request.get_json()
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    password = data.get("password")

    if not email or not first_name or not last_name or not password:
        return {"message": "Missing required fields (email, first name, last name, password).","status":400}

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"message": "User with this email already exists.","status":409}

    hashed_password = generate_password_hash(password)

    new_admin = User(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=hashed_password,
        is_admin=True,
        img_url=current_app.config['DEFAULT_PROFILE_PIC']
    )

    db.session.add(new_admin)
    db.session.commit()

    return {"message": "Admin account created successfully!","status":201, "data": new_admin.user_id}


def block_user(userid):
    current_user_id = get_jwt_identity()

    admin = User.query.filter_by(user_id = current_user_id).first()
    if not admin or (not admin.is_admin and not admin.is_super_admin):
        return {"message": "Unauthorized. Only admins/superadmins can blok users.","status":403}
    
    
    user = User.query.filter_by(user_id = userid).first()
    
    if not user:
        return {"message": "User not found.","status":404}

    if user.is_super_admin:
        return {"message": "You cannot block a superadmin.","status":403}  

    # Block the user
    user.is_blocked = True
    db.session.commit()

    return {"message": f"User {user.email} has been blocked successfully.","status":200}

def promote(userid):
    current_user_id = get_jwt_identity()

    admin = User.query.filter_by(user_id = current_user_id).first()
    if not admin or (not admin.is_super_admin):
        return {"message": "Unauthorized. Only superadmins can promote users.","status":403}
    
    
    user = User.query.filter_by(user_id = userid).first()
    
    if not user:
        return {"message": "User not found.","status":404}

    if user.is_super_admin or user.is_admin:
        return {"message": "he is already an admin","status":403}  

    # Block the user
    user.is_admin = True
    db.session.commit()

    return {"message": f"User {user.email} has been promoted succefully.","status":200}

def turn(userid):
    current_user_id = get_jwt_identity()

    admin = User.query.filter_by(user_id = current_user_id).first()
    if not admin or (not admin.is_super_admin):
        return {"message": "Unauthorized. Only superadmins can turn users.","status":403}
    
    
    user = User.query.filter(User.user_id == userid, User.is_super_admin == False).first()
    
    if not user:
        return {"message": "User not found.","status":404}

    if not user.is_admin:
        return {"message": "he is already a client","status":403}  

    # Block the user
    user.is_admin = False
    db.session.commit()

    return {"message": f"User {user.email} has been turned into client succefully.","status":200}


def unblock_user(userid):
    current_user_id = get_jwt_identity()

    admin = User.query.filter_by(user_id = current_user_id).first()
    if not admin or (not admin.is_admin and not admin.is_super_admin):
        return {"message": "Unauthorized. Only admins/superadmins can unblock users.","status":403}
    
    user = User.query.filter_by(user_id = userid).first()
    
    if not user:
        return {"message": "User not found.","status":404}

    if user.is_super_admin:
        return {"message": "You cannot block a superadmin.","status":403}  

    # Block the user
    user.is_blocked = False
    db.session.commit()

    return {"message": f"User {user.email} has been unblocked successfully.","status":200}

#----------------------------------------------------------------------------------------------------

def get_all_users():
    current_user_id = get_jwt_identity()
    admin_user = User.query.filter_by(user_id = current_user_id).first()

    if not admin_user or not (admin_user.is_admin or admin_user.is_super_admin):
        return {"message": "Unauthorized. Only admins and superadmins can access this route.","status":403} 
    
    clients = User.query.filter_by(is_super_admin=False).all()
    users_list = [client.toDic() for client in clients]

    return {"message": "Success","status":200,"data": users_list}
#----------------------------------------------------------------------------------------------------

