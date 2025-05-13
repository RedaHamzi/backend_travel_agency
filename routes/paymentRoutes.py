from flask import Blueprint, request, jsonify
from controllers.payement_controller import *
from models.user import User
from models.payment import Payment
from flask_jwt_extended import jwt_required
from datetime import datetime

payment_bp = Blueprint('payment_bp', __name__)


@payment_bp.route('/get-payments-by-filter', methods=['GET'])
@jwt_required()
def get_by_filter():
    curr_user = User.query.filter_by(user_id=int(get_jwt_identity())).first()
    
    # Only admin/super-admin can filter other users' payments
    if not (curr_user.is_super_admin or curr_user.is_admin):
        # Non-admin users can only filter their own payments
        filters = request.args.to_dict()
        filters['user_id'] = curr_user.user_id
    else:
        filters = request.args.to_dict()
    
    # Convert date strings to date objects if present
    if 'start_date' in filters:
        try:
            filters['start_date'] = datetime.strptime(filters['start_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Invalid start_date format. Use YYYY-MM-DD', 'status': 400})
    
    if 'end_date' in filters:
        try:
            filters['end_date'] = datetime.strptime(filters['end_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Invalid end_date format. Use YYYY-MM-DD', 'status': 400})
    
    # Convert is_valid to boolean if present
    if 'is_valid' in filters:
        if filters['is_valid'].lower() in ['true', '1', 't']:
            filters['is_valid'] = True
        elif filters['is_valid'].lower() in ['false', '0', 'f']:
            filters['is_valid'] = False
        else:
            return jsonify({'message': 'Invalid is_valid value. Use true/false', 'status': 400})
    
    return jsonify(get_payments_by_filter(filters))

# this one is for simulated payment on the website
@payment_bp.route('/create-payment', methods=['POST'])
@jwt_required()
def create():
    data= request.json
    return jsonify(create_payment1(data))
 
@payment_bp.route('/get-payments', methods=['GET'])
@jwt_required()
def get_all():
    curr = User.query.filter_by(user_id = int(get_jwt_identity())).first()
    if curr.is_super_admin or curr.is_admin :
         return jsonify(get_all_payments())
    return jsonify({'message' : 'Unautherized', 'status':401})

@payment_bp.route('/get-payment/<int:payment_id>', methods=['GET'])
@jwt_required()
def get_one(payment_id):
    curr = User.query.filter_by(user_id = int(get_jwt_identity())).first()
    if curr.is_super_admin or curr.is_admin :
         return jsonify(get_payment(payment_id))
    return jsonify({'message' : 'Unautherized', 'status':401})

@payment_bp.route('/update-payment/<int:payment_id>', methods=['PUT']) 
@jwt_required()
def update(payment_id):
    data= request.json

    curr = Payment.query.filter_by(user_id = int(get_jwt_identity())).first()
    if curr :
        return jsonify(update_payment(payment_id,data))
    return jsonify({'message' : 'Unautherized', 'status':401})

@payment_bp.route('/delete-payment/<int:payment_id>', methods=['PUT'])
@jwt_required()
def delete(payment_id):
    curr = Payment.query.filter_by(user_id = int(get_jwt_identity())).first()
    if curr :
        return jsonify(delete_payment(payment_id))
    return jsonify({'message' : 'Unautherized', 'status':401})
 
@payment_bp.route("/validate-payment/<int:id>", methods=['PUT'])
@jwt_required()
def valid(id):
    curr = User.query.filter_by(user_id = int(get_jwt_identity())).first()
    if curr.is_admin or curr.is_super_admin:
        return jsonify(validate_payment(id))
    return jsonify({'message' : 'Unautherized', 'status':401})
