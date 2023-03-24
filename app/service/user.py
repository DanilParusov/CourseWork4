from app.dao.user import UserDAO
from app.helpers import make_user_password_hash


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_item_by_id(self, pk):
        user = UserDAO(self.dao).get_by_id(pk)
        return user

    def get_item_by_email(self, email):
        user = UserDAO(self.dao).get_by_email(email)
        return user

    def get_all_users(self):
        return self.dao.get_all()

    def create(self, new_pd):
        user_password = new_pd.get("password")
        if user_password:
            new_pd["password"] = make_user_password_hash(user_password)
        user = {
            "password": user_password
        }
        user = self.dao.create(user)
        return user

    def update(self, new_pd):
        user = UserDAO(self.dao).update(new_pd)
        return user


    def update_password(self, new_pd):
        user_password_1 = new_pd.get("password_1")
        user_password_2 = new_pd.get("password_2")
        return ""