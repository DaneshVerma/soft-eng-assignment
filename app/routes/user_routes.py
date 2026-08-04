from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        user = UserService.create_user(data)
        return jsonify({
            "success": True,
            "data": user.to_dict()
        }), 201
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

@user_bp.route('', methods=['GET'])
def get_users():
    try:
        users = UserService.get_all_users()
        return jsonify({
            "success": True,
            "data": [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({
                "success": False,
                "error": "User not found"
            }), 404
        return jsonify({
            "success": True,
            "data": user.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
