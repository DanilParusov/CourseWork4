from app.dao.model.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, mid):
        return self.session.query(Movie).get(mid)

    def get_all(self):
        return self.session.query(Movie).all()

    def get_all_with_order(self):
        return self.session.query(Movie).order_by(Movie.year.asc()).all()

    def get_all_with_page_limit(self, page_limit):
        return self.session.query(Movie).limit(page_limit).all()

    def get_all_with_limit_and_order(self, page_limit):
        return self.session.query(Movie).order_by(Movie.year.asc()).limit(page_limit).all()
