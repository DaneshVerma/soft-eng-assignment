from typing import Any
from sqlalchemy import or_
from flask_sqlalchemy.pagination import Pagination
from app.extensions import db
from app.models.user import User
from app.errors import ValidationError, NotFoundError
from app.utils.validation import validate_user_data, validate_email_uniqueness

class UserService:
    """Service layer for handling user-related business logic."""

    @staticmethod
    def create_user(data: dict[str, Any]) -> User:
        """
        Create a new user.

        Args:
            data: A dictionary containing 'name', 'email', and 'role'.

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

        new_user = User(
            name=data.get('name'),
            email=email,
            role=data.get('role')
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get_all_users(page: int = 1, limit: int = 10, search: str | None = None) -> Pagination:
        """
        Retrieve a paginated list of users, optionally filtered by a search term.

        Args:
            page: The page number to retrieve. Defaults to 1.
            limit: The number of items per page. Defaults to 10.
            search: An optional search term to filter users by name or email.

        Returns:
            A SQLAlchemy Pagination object containing the users.
        """
        query = User.query

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    User.name.ilike(search_term),
                    User.email.ilike(search_term)
                )
            )

        return query.paginate(page=page, per_page=limit, error_out=False)

    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """
        Retrieve a single user by their ID.

        Args:
            user_id: The ID of the user.

        Returns:
            The User instance if found.

        Raises:
            NotFoundError: If the user does not exist.
        """
        user = db.session.get(User, user_id)
        if not user:
            raise NotFoundError("User not found")
        return user
