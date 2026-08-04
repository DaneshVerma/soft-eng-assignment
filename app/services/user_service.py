from app.extensions import db
from app.models.user import User

class UserService:
    @staticmethod
    def create_user(data):
        try:
            new_user = User(
                name=data.get('name'),
                email=data.get('email'),
                role=data.get('role')
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)
