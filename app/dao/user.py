import json

from app.dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_by_id(self, pk):
        return self.session.query(User).filter(User.id == pk).one_or_none()

    def get_by_email(self, email):
        return self.session.query(User).filter(User.email == email).one_or_none()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, user_d):
        user_d = json.loads(user_d)
        ent = User(**user_d)
        self.session.add(ent)
        self.session.commit()
        return ent


    def update(self, new_pd):
        user = self.get_by_id(new_pd.get('id'))
        if user:
            if new_pd.get('password'):
                user.password = new_pd.get('password')
            if new_pd.get('email'):
                user.email = new_pd.get('email')
            if new_pd.get('name'):
                user.name = new_pd.get('name')
            if new_pd.get('surname'):
                user.surname = new_pd.get('surname')
            if new_pd.get('favorite_genre'):
                user.favorite_genre = new_pd.get('favorite_genre')

        self.session.add(user)
        self.session.commit()