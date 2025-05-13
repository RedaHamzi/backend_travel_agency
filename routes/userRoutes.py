# /routes/userRoutes
from flask import Blueprint, request, jsonify
from controllers.user_controller import create_user_1,login,create_user_2,get_user, remove_admin,get_user_by_filter,create_super_admin,create_admin, block_user, unblock_user, get_all_users,promote,turn, forgot_password_enter_email_, forgot_password_verify_code_, forgot_password_reset_password_, update_user_
from models.user import User
from models import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from pics_handler import upload_pfp, delete_pfp
import json 

user_bp = Blueprint('user_bp', __name__)


#signup routes
@user_bp.route("/verify-reg", methods=["POST"])
def verify_reg():
    data = request.json
    return jsonify(create_user_1(data))

@user_bp.route("/add-client", methods=["POST"])
def add_client():
    data = request.json
    return jsonify(create_user_2(data))


#login

@user_bp.route("/login", methods=["POST"])
def login_user():
    data = request.json
    return jsonify(login(data))


#test to understand the kinda private route "test", this route is accessed only by admins 

# @user_bp.route("/test")
# @jwt_required()
# def test():
#     current_user = User.query.filter_by(user_id = int(get_jwt_identity())).first()
#     if current_user.is_super_admin == False and current_user.is_admin == False:
#         return {'error': 'Unauthorized'}, 401 
#     else :
#         return jsonify(current_user.toDic()),200


@user_bp.route('/get-user/<int:user_id>')
@jwt_required()
def get_user_by_id(user_id):
    curr = User.query.filter_by(user_id = int(get_jwt_identity())).first()
    if curr.is_admin == True or curr.is_super_admin == True or curr.user_id == user_id:
        return jsonify(get_user(user_id))
    return jsonify({"message": "Unautorized","status":401})






@user_bp.route('/remove-admin/<int:admin_id>', methods=["PUT"])
@jwt_required()
def remove(admin_id):
    curr = User.query.filter_by(user_id = int(get_jwt_identity())).first()
    if curr.is_super_admin == True:
        return jsonify(remove_admin(admin_id))
    return jsonify({"message": "Unautorized","status":401})


@user_bp.route('/get-users-by-filter', methods=["GET"])
@jwt_required() 
def get_users_filter():
    data = request.args
    curr = User.query.filter_by(user_id = int(get_jwt_identity())).first()
    if curr.is_admin == True or curr.is_super_admin == True:
        return jsonify(get_user_by_filter(data))
    return jsonify({"message": "Unautorized","status":401})


@user_bp.route('/createsuperadmin', methods=['POST'])
def create_super_admin_route():
    return jsonify(create_super_admin()) 

@user_bp.route('/create-admin', methods=['POST'])
@jwt_required()
def create_admin_route():

    current_user = User.query.filter_by(user_id = int(get_jwt_identity())).first()
    if current_user.is_super_admin == False:
        return jsonify({"message": "Unautorized","status":401})
    
    return jsonify(create_admin())

@user_bp.route('/block-user/<int:user_id>', methods=['PUT'])
@jwt_required()
def block_user_route(user_id):
    return jsonify(block_user(user_id))

@user_bp.route('/promote-to-admin/<int:user_id>', methods=['PUT'])
@jwt_required()
def promote_to_admin_route(user_id):
    return jsonify(promote(user_id))

@user_bp.route('/turn-to-user/<int:user_id>', methods=['PUT'])
@jwt_required()
def turn_to_user(user_id):
    return jsonify(turn(user_id))

@user_bp.route('/unblock-user/<int:user_id>', methods=['PUT'])
@jwt_required()
def unblock_user_route(user_id):
    return jsonify(unblock_user(user_id))

@user_bp.route('/get-all-users', methods=['GET'])
@jwt_required()
def get_all_clients_route():
    return jsonify(get_all_users())


#forgot password
@user_bp.route('/forgot-password/enter-email', methods=['POST'])
def forgot_password_enter_email():
    data = request.json
    return jsonify(forgot_password_enter_email_(data))

@user_bp.route('/forgot-password/verify-code', methods=['POST'])
def forgot_password_verify_code():
    data = request.json
    return jsonify(forgot_password_verify_code_(data))


@user_bp.route('/forgot-password/reset-password', methods=['POST'])
def forgot_password_reset_password():
    data = request.json
    return jsonify(forgot_password_reset_password_(data))



#update user
@user_bp.route('/update-user', methods=['PUT'])
@jwt_required()
def update_user():
    id = int(get_jwt_identity())
    data = json.loads(request.form.get("json"))
    file = request.files.get("img_url")
    return jsonify(update_user_(data,file, id))


@user_bp.route('/delete-pfp', methods=['DELETE'])
@jwt_required()
def del_pfp():
    user = User.query.filter_by(user_id = int(get_jwt_identity())).first()
    return jsonify(delete_pfp(user))


