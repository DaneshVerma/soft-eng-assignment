from flask import Blueprint, request, jsonify
from app.services.user_service import UserService

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    user = UserService.create_user(data)
    return jsonify({
        "success": True,
        "data": user.to_dict()
    }), 201

@user_bp.route('', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    search = request.args.get('search', None)

    paginated_users = UserService.get_all_users(page=page, limit=limit, search=search)
    
    return jsonify({
        "success": True,
        "data": [user.to_dict() for user in paginated_users.items],
        "page": paginated_users.page,
        "limit": paginated_users.per_page,
        "total": paginated_users.total,
        "total_pages": paginated_users.pages
    }), 200

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserService.get_user_by_id(user_id)
    return jsonify({
        "success": True,
        "data": user.to_dict()
    }), 200
