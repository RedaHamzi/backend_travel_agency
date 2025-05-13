from flask import Blueprint,request,jsonify
from flask import Blueprint, request, jsonify
from controllers.ticket_controller import get_tickets_by_filter, update_ticket,delete_ticket,add_ticket
from models.ticket import Ticket
from models import db
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

ticket_bp = Blueprint('ticket_bp',__name__)





@ticket_bp.route('/get-tickets-by-filter', methods=["GET"])
def get_tickets_by_filter_route():
    data = request.args
    return jsonify(get_tickets_by_filter(data))




@ticket_bp.route('/update-ticket/<int:ticket_id>', methods=["PUT"])
@jwt_required()
def update_ticket_route(ticket_id):
    data = request.json
    user = User.query.filter_by(user_id=int(get_jwt_identity())).first()
    if user.is_admin == False and user.is_super_admin == False:
        return jsonify({'message': 'Unauthorized',"status":401})
    return jsonify(update_ticket(data,ticket_id))




@ticket_bp.route('/delete-ticket/<int:ticket_id>', methods=["DELETE"])
@jwt_required()
def delete_ticket_route(ticket_id):
    user = User.query.filter_by(user_id=int(get_jwt_identity())).first()
    if user.is_admin == False and user.is_super_admin == False:
        return jsonify({"message": "Unautorized","status":401})
    return jsonify(delete_ticket(ticket_id)) 



@ticket_bp.route('/add-ticket', methods=["POST"])
@jwt_required()
def add_ticket_route():
    data = request.json
    user = User.query.filter_by(user_id=int(get_jwt_identity())).first()
    if user.is_admin == False and user.is_super_admin == False:
        return jsonify({'message': 'Unauthorized',"status":401})
    return jsonify(add_ticket(data))

   
