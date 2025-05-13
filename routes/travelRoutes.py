# /routes/travelRoutes
from flask import Blueprint,request,jsonify, json
from controllers.travel_controller import create_travel, remove_travel, update_travel_, filter_travels
from models.user import User
  
from models import db
from flask_jwt_extended import jwt_required, get_jwt_identity

travel_bp = Blueprint('travel_bp',__name__)
 
@travel_bp.route('/add-travel',methods=['POST'])
@jwt_required()
def add_travel():
    data = json.loads(request.form.get("json"))
    file = request.files.get("img_url")
    user = User.query.filter_by(user_id = int(get_jwt_identity())).first()
    if user.is_admin == True or user.is_super_admin == True:
        return jsonify(create_travel(data, file))
    return jsonify({"message": "Unautorized","status":401})


@travel_bp.route('/update-travel/<int:id>', methods=['PUT'])
@jwt_required()
def update_travel(id):
    user = User.query.filter_by(user_id=int(get_jwt_identity())).first()
    if user.is_admin == False and user.is_super_admin == False:
        return jsonify({"message": "Unautorized","status":401})
    data = json.loads(request.form.get("json"))
    file = request.files.get("img_url")
    return jsonify(update_travel_(data,file, id))




@travel_bp.route('/remove-travel/<int:id>', methods=["DELETE"])
@jwt_required()
def remove(id):
    curr = User.query.filter_by(user_id = int(get_jwt_identity())).first()
    if curr.is_super_admin == False and curr.is_admin == False:
        return jsonify({"message": "Unautorized","status":401})
    return jsonify(remove_travel(id))
        
    


@travel_bp.route('/filter-travels', methods=["GET"])
def get_users_filter():
    data = request.args
    return jsonify(filter_travels(data))
