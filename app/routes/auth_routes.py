from typing import Any
from flask import Blueprint, request, Response
from app.services.auth_service import AuthService
from app.utils.responses import success_response

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register() -> tuple[Response, int]:
    """
    Register a new user.

    Returns:
        JSON response with the created user data and HTTP status 201.
    """
    data: dict[str, Any] = request.get_json() or {}
    user = AuthService.register(data)
    return success_response(data=user.to_dict(), status_code=201)

@auth_bp.route('/login', methods=['POST'])
def login() -> tuple[Response, int]:
    """
    Authenticate a user and return a JWT.

    Returns:
        JSON response with the JWT token and user data, HTTP status 200.
    """
    data: dict[str, Any] = request.get_json() or {}
    token, user = AuthService.login(data)
    return success_response(
        data={
            "token": token,
            "user": user.to_dict()
        },
        status_code=200
    )
