from flask import Blueprint, request, jsonify
import json
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from models.user import User

 
from controllers.accomodation_controller import *
"""(
    create_accomodation,
    filter_accomodations,
    get_accomodation,
    update_accomodation,
    delete_accomodation
)"""
 

accomodation_bp = Blueprint('accomodation_bp', __name__)  # Fixed here ✅


# CREATE
@accomodation_bp.route('/create-accomodation', methods=['POST'])
@jwt_required()
def create_acc():
    data = json.loads(request.form.get("json"))
    file = request.files.get("img_url")
    curr = User.query.filter_by(user_id = int(get_jwt_identity())).first()
    if curr.is_super_admin or curr.is_admin :
        return jsonify(create_accomodation(data, file))
    return jsonify({'message' : 'Unautherized', 'status':401})
   

# Get all
@accomodation_bp.route('/filter-accomodations', methods=['GET'])
def get_all_acc():
    return jsonify(filter_accomodations(request.args))

# READ (Get one by ID)
@accomodation_bp.route('/get-accomodation/<int:id>', methods=['GET'])
def get_one_acc(id):
    return jsonify(get_accomodation(id))
    

# UPDATE
@accomodation_bp.route('/update-accomodation/<int:id>', methods=['PUT'])
@jwt_required()
def update_acc(id):
    data = json.loads(request.form.get("json"))
    file = request.files.get("img_url")
    curr = User.query.filter_by(user_id = int(get_jwt_identity())).first()
    if curr.is_super_admin or curr.is_admin :
        return jsonify(update_accomodation(id,data, file))
    return jsonify({'message' : 'Unautherized', 'status':401})

# DELETE
@accomodation_bp.route('/delete-accomodation/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_acc(id):
    curr = User.query.filter_by(user_id = int(get_jwt_identity())).first()
    if curr.is_super_admin or curr.is_admin :
        return jsonify(delete_accomodation(id))
    return jsonify({'message' : 'Unautherized', 'status':401})
