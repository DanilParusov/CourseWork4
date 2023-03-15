from flask_restx import Resource, Namespace

from app.dao.model.director import DirectorSchema
from app.implemented import director_service

director_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        return directors_schema.dump(director_service.get_all()), 200


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did):
        return director_schema.dump(director_service.get_one(did)), 200