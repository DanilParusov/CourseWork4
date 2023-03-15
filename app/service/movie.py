from app.dao.movie import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.dao = dao

    def get_one(self, mid):
        return self.dao.get_one(mid)

    def get_all(self, filters):
        if filters.get("page") is not None and filters.get("status") == "new":
            movies = self.dao.get_all_with_limit_and_order(filters.get("page"))
        elif filters.get("page") is not None:
            movies = self.dao.get_all_with_page_limit(filters.get("page"))
        elif filters.get("status") == "new":
            movies = self.dao.get_all_with_order()
        else:
            movies = self.dao.get_all()
        return movies
