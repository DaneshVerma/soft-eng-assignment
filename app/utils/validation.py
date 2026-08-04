import re
from typing import Any
from app.errors import ValidationError
from app.models.user import User

def validate_user_data(data: dict[str, Any] | None) -> None:
    """
    Validate the incoming user data for required fields and valid formats.

    Args:
        data: The dictionary containing user data.

    Raises:
        ValidationError: If data is missing or invalid.
    """
    if not data:
        raise ValidationError("No input data provided")
    
    required_fields = ['name', 'email', 'role']
    for field in required_fields:
        if not data.get(field):
            raise ValidationError(f"Field '{field}' is required")
            
    email = data.get('email')
    if not isinstance(email, str):
        raise ValidationError("Email must be a string")
        
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        raise ValidationError("Invalid email format")

def validate_email_uniqueness(email: str) -> None:
    """
    Check if the email is already registered in the database.

    Args:
        email: The email string to check.

    Raises:
        ValidationError: If the email already exists.
    """
    if User.query.filter_by(email=email).first():
        raise ValidationError("Email already registered")
