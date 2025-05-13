from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from models.review import Review
from controllers.review_controller import *

review_bp = Blueprint('review_bp', __name__)

# CREATE
@review_bp.route('/create-review', methods=['POST'])
@jwt_required()
def create():
    data = request.json
    curr = User.query.filter_by(user_id=int(get_jwt_identity())).first()
    if curr and (curr.is_super_admin or curr.is_admin):
        return jsonify(create_review(data))
    return jsonify({'message': 'Unauthorized',"status":401})

# GET ALL
@review_bp.route('/get-reviews', methods=['GET'])
def get_all():
    return jsonify(get_all_reviews())

# GET ONE
@review_bp.route('/get-review/<int:review_id>', methods=['GET'])
def get_one(review_id):
    return jsonify(get_review(review_id))

# UPDATE
@review_bp.route('/update-review/<int:review_id>', methods=['PUT'])
@jwt_required()
def update(review_id):
    data = request.json
    rev = Review.query.filter_by(user_id = int(get_jwt_identity())).first()
    if rev:
        return jsonify(update_review(review_id, data))
    return jsonify({'message': 'Unauthorized',"status":401})

# DELETE
@review_bp.route('/delete-review/<int:review_id>', methods=['DELETE'])
@jwt_required()
def delete(review_id):
    curr = User.query.filter_by(user_id=int(get_jwt_identity())).first()
    rev = Review.query.filter_by(user_id = int(get_jwt_identity())).first()
    if rev or (curr.is_super_admin or curr.is_admin):
        return jsonify(delete_review(review_id))
    return jsonify({'message': 'Unauthorized',"status":401})
