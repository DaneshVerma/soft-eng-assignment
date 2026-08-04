import bcrypt
from flask_jwt_extended import create_access_token
from app.extensions import db
from app.models.user import User
from app.errors import ValidationError, APIError
from app.utils.validation import validate_user_data

class AuthService:
    @staticmethod
    def register(data):
        validate_user_data(data)
        password = data.get('password')
        if not password or len(password) < 6:
            raise ValidationError("Password must be at least 6 characters long")

        if User.query.filter_by(email=data.get('email')).first():
            raise ValidationError("Email already registered")

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        new_user = User(
            name=data.get('name'),
            email=data.get('email'),
            password_hash=hashed,
            role=data.get('role')
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def login(data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise ValidationError("Email and password are required")

        user = User.query.filter_by(email=email).first()
        if not user or not user.password_hash:
            raise APIError("Invalid email or password", status_code=401)
            
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            raise APIError("Invalid email or password", status_code=401)

        access_token = create_access_token(identity=str(user.id))
        return access_token, user
