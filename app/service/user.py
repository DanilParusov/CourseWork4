from app.dao.user import UserDAO
from app.helpers import generate_password_digest


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
        users = UserDAO(self.dao).get_all()
        return users

    def create(self, new_pd):
        user_password = new_pd.get("password")
        if user_password:
            new_pd["password"] = generate_password_digest(user_password)
        user = UserDAO(self.dao).create(user_password)
        return user

    def update(self, new_pd):
        user = UserDAO(self.dao).update(new_pd)
        return user


    def update_password(self, new_pd):
        user_password_1 = new_pd.get("password_1")
        user_password_2 = new_pd.get("password_2")