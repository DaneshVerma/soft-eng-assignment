from typing import Any
from flask import Blueprint, request, Response
from flask_jwt_extended import jwt_required
from app.services.user_service import UserService
from app.utils.responses import success_response

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('', methods=['POST'])
@jwt_required()
def create_user() -> tuple[Response, int]:
    """
    Create a new user.
    
    Returns:
        JSON response with the created user data and HTTP status 201.
    """
    data: dict[str, Any] = request.get_json() or {}
    user = UserService.create_user(data)
    return success_response(data=user.to_dict(), status_code=201)

@user_bp.route('', methods=['GET'])
@jwt_required()
def get_users() -> tuple[Response, int]:
    """
    Get a paginated list of users, optionally filtered by search term.
    
    Returns:
        JSON response with the list of users, pagination metadata, and HTTP status 200.
    """
    page: int = request.args.get('page', 1, type=int)
    limit: int = request.args.get('limit', 10, type=int)
    search: str | None = request.args.get('search', None)

    paginated_users = UserService.get_all_users(page=page, limit=limit, search=search)
    
    return success_response(
        data=[user.to_dict() for user in paginated_users.items],
        status_code=200,
        page=paginated_users.page,
        limit=paginated_users.per_page,
        total=paginated_users.total,
        total_pages=paginated_users.pages
    )

@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id: int) -> tuple[Response, int]:
    """
    Get a single user by their ID.
    
    Args:
        user_id: The ID of the user.
        
    Returns:
        JSON response with the user data and HTTP status 200.
    """
    user = UserService.get_user_by_id(user_id)
    return success_response(data=user.to_dict(), status_code=200)
