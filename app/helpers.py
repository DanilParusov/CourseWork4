import base64
import hashlib
import hmac
import datetime
import calendar
import jwt

from typing import Union
from flask import current_app, request, abort



secret = 's3cR$eT'
algo = 'HS256'

def generate_password_digest(password):
    return hashlib.pbkdf2_hmac(
        hash_name="sha256",
        password=password.encode("utf-8"),
        salt=current_app.config["PWD_HASH_SALT"],
        iterations=current_app.config["PWD_HASH_ITERATIONS"],
    )

def get_password_hash(password: str) -> str:
    return base64.b64encode(generate_password_digest(password)).decode('utf-8')

# сравнение паролей

def compare_password(hash_password: Union[str, bytes], password: str) -> bool:
    return hmac.compare_digest(
        base64.b64decode(hash_password),
        generate_password_digest(password)
    )

# проверка токена
def check_token(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        return func(*args, **kwargs)
    return wrapper

# проверка права администратора, на изменение
def admin_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            user = jwt.decode(token, secret, algorithms=[algo])
            role = user.get("role")
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        if role != "admin":
            abort(403)
        return func(*args, **kwargs)
    return wrapper


def generate_token(data):
    min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    data["exp"] = calendar.timegm(min30.timetuple())
    access_token = jwt.encode(data, secret, algorithm=algo)
    days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
    data["exp"] = calendar.timegm(days130.timetuple())
    refresh_token = jwt.encode(data, secret, algorithm=algo)
    tokens = {"access_token": access_token, "refresh_token": refresh_token}
    return tokens, 202

def login_user(reg_json, user):
    user_email = reg_json.get("email")
    user_password = reg_json.get("password")
    if user_email and user_password:
        password_hashed = user["password"]
        reg_json["role"] = user["role"]
        reg_json["id"] = user["id"]
        if compare_password(password_hashed, user_password):
            return generate_token(reg_json)

def refresh_user_token(reg_json):
    refresh_token = reg_json.get("refresh_token")
    jwt_decode = jwt.decode(refresh_token, secret, algorithms=[algo])
    data = jwt_decode(refresh_token)
    if data:
        tokens = generate_token(data)
        return tokens