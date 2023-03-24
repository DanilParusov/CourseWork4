import flask
from flask_restx import Api

from app.config import Config
from app.setup_db import db
from app.views.director import director_ns
from app.views.genre import genre_ns
from app.views.movie import movie_ns
from app.views.user import user_ns
from app.views.auth import auth_ns


def create_app(config_object):
    app = flask.Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)


app = create_app(Config())

if __name__ == '__main__':
    app.run()