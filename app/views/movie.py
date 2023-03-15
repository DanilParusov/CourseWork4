from flask import request
from flask_restx import Resource, Namespace
from app.dao.model.movie import MovieSchema
from app.implemented import movie_service

movie_ns = Namespace('movies')

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        page = request.args.get("page")
        status = request.args.get("status")
        filters = {
            "page": page,
            "status": status,
        }
        return movies_schema.dump(movie_service.get_all(filters)), 200


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid):
        return movie_schema.dump(movie_service.get_one(mid)), 200