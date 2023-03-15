from flask_restx import abort, Namespace, Resource
from flask import request

from app.helpers import login_user, refresh_user_token
from app.service.user import UserService
from app.setup_db import db

auth_ns = Namespace('auth')
secret = 's3cR$eT'
algo = 'HS256'


@auth_ns.route('/login')
class AuthView(Resource):
    def post(self):
        req_json = request.json
        email = req_json.get("email", None)
        password = req_json.get("password", None)
        if None in [email, password]:
            abort(400)

        user = UserService(db.session).get_item_by_email(email=email)
        tokens = login_user(request.json, user)
        return tokens, 201


    def put(self):
        req_json = request.json
        if None in req_json:
            abort(400)

        tokens = refresh_user_token(req_json)
        return tokens, 200

@auth_ns.route('/register')
class AuthRegView(Resource):
    def post(self):
        req_json = request.json
        if None in req_json:
            abort(400, "не корректный запрос")
