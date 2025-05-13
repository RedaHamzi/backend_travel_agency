#/routes/orderRoutes.py
from flask import Blueprint, request, jsonify, json
from controllers.order_controller import add_order, cancel_order, update_order, get_order_by_filter
from models.user import User
from models.order import Order
from flask_jwt_extended import jwt_required, get_jwt_identity

order_bp = Blueprint('order_bp', __name__)


@order_bp.route('/add-order',methods=['POST'])
@jwt_required()
def create():
    data = request.json
    return jsonify(add_order(data))


@order_bp.route('/update-order/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    data = request.json
    return jsonify(update_order(data,id))



@order_bp.route('/cancel-order/<int:id>', methods=["PUT"])
@jwt_required()
def remove(id):
    curr = Order.query.filter_by(user_id = int(get_jwt_identity())).first()
    if curr:
        return jsonify(cancel_order(id))
    return jsonify({'message' : 'Unautherized', 'status':401})
        
    
  

@order_bp.route('/filter-orders', methods=["GET"])
@jwt_required() 
def filter_orders():
    return jsonify(get_order_by_filter(request.args))

