from app.extensions import db
from app.models.user import User
from app.errors import ValidationError, NotFoundError
from app.utils.validation import validate_user_data

class UserService:
    @staticmethod
    def create_user(data):
        validate_user_data(data)

        if User.query.filter_by(email=data.get('email')).first():
            raise ValidationError("Email already registered")

        new_user = User(
            name=data.get('name'),
            email=data.get('email'),
            role=data.get('role')
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get_all_users(page=1, limit=10, search=None):
        query = User.query

        if search:
            from sqlalchemy import or_
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    User.name.ilike(search_term),
                    User.email.ilike(search_term)
                )
            )

        return query.paginate(page=page, per_page=limit, error_out=False)

    @staticmethod
    def get_user_by_id(user_id):
        user = db.session.get(User, user_id)
        if not user:
            raise NotFoundError("User not found")
        return user
