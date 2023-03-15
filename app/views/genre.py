from flask_restx import Resource, Namespace

from app.dao.model.genre import GenreSchema
from app.implemented import genre_service

genre_ns = Namespace('genres')

genres_schema = GenreSchema(many=True)
genre_schema = GenreSchema()


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        return genres_schema.dump(genre_service.get_all()), 200


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid):
        return genre_schema.dump(genre_service.get_one(gid)), 200