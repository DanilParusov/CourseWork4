from flask import request, abort, g
from flask_restx import Resource, Namespace

from app.dao.model.user import UserSchema
from app.implemented import user_service
from app.helpers import auth_required


user_ns = Namespace('users')

users_schema = UserSchema(many=True)
user_schema = UserSchema()

@user_ns.route("/")
class UsersView(Resource):
    @auth_required
    def get(self):
        """Get all users"""
        email = g.email
        return users_schema.dump(user_service.get_item_by_email(email))


@user_ns.route("/<int:user_id>")
class UserView(Resource):
    def get(self, user_id: int):
        """Get user by id"""
        return user_schema.dump(user_service.get_item_by_id(user_id))


    def patch(self, user_id: int):
        req_json = request.json
        if not req_json:
            abort(400, "Повторите запрос")
        if not req_json.get("id"):
            req_json['id'] = user_id
        user_service.update(req_json)
        return ""

@user_ns.route("/password/<int:user_id>")
class UserPatchView(Resource):
    # @admin_required
    def put(self, user_id:int):
        req_json = request.json
        password_1 = req_json.get("password_1", None)
        password_2 = req_json.get("password_2", None)
        if None in [password_1, password_2]:
            abort(400, "Повторите запрос")
        if not password_1 or not password_2:
            abort(400, "Повторите запрос")
        if not req_json.get("id"):
            req_json['id'] = user_id

        user_service.update_password(req_json)
        return ""
