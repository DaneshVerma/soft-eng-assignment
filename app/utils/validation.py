import re
from app.errors import ValidationError

def validate_user_data(data):
    if not data:
        raise ValidationError("No input data provided")
    
    required_fields = ['name', 'email', 'role']
    for field in required_fields:
        if not data.get(field):
            raise ValidationError(f"Field '{field}' is required")
            
    email = data.get('email')
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        raise ValidationError("Invalid email format")
