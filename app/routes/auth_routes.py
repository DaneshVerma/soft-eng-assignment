from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = AuthService.register(data)
    return jsonify({
        "success": True,
        "data": user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    token, user = AuthService.login(data)
    return jsonify({
        "success": True,
        "data": {
            "token": token,
            "user": user.to_dict()
        }
    }), 200
