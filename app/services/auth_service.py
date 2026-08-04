import bcrypt
from typing import Any
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User
from app.errors import ValidationError, APIError
from app.utils.validation import validate_user_data, validate_email_uniqueness

class AuthService:
    """Service layer for handling authentication business logic."""

    @staticmethod
    def register(data: dict[str, Any]) -> User:
        """
        Register a new user in the system.

        Args:
            data: A dictionary containing 'name', 'email', 'password', and 'role'.

        Returns:
            The created User instance.
            
        Raises:
            ValidationError: If validation fails or email already exists.
        """
        validate_user_data(data)
        
        email = data.get('email')
        if not isinstance(email, str):
            raise ValidationError("Email must be a string")
            
        validate_email_uniqueness(email)

        password = data.get('password')
        if not password or len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long")

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        new_user = User(
            name=data.get('name'),
            email=email,
            password_hash=hashed,
            role=data.get('role')
        )
        db.session.add(new_user)
        db.session.commit()
        
        return new_user

    @staticmethod
    def login(data: dict[str, Any]) -> tuple[str, User]:
        """
        Authenticate a user and return a JWT access token.

        Args:
            data: A dictionary containing 'email' and 'password'.

        Returns:
            A tuple containing the JWT token string and the authenticated User instance.
            
        Raises:
            ValidationError: If email or password is not provided.
            APIError: If authentication fails due to invalid credentials.
        """
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise ValidationError("Email and password are required")

        user = User.query.filter_by(email=email).first()
        if not user or not user.password_hash:
            raise APIError("Invalid email or password", status_code=401)
            
        if not isinstance(password, str):
            raise ValidationError("Password must be a string")

        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            raise APIError("Invalid email or password", status_code=401)

        access_token = create_access_token(identity=str(user.id))
        return access_token, user
