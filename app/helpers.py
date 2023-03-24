import base64
import hashlib
import hmac
import datetime
import calendar
import jwt

from typing import Union
from flask import current_app, request, abort
from app.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS



secret = 's3cR$eT'
algo = 'HS256'


def make_user_password_hash(password):
    return base64.b64encode(hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
    ))

def get_password_hash(password: str) -> str:
    return base64.b64encode(make_user_password_hash(password)).decode('utf-8')

# сравнение паролей

def compare_password(hash_password: Union[str, bytes], password: str) -> bool:
    return hmac.compare_digest(
        base64.b64decode(hash_password),
        make_user_password_hash(password)
    )

# проверка токена
def check_token(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
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
        password_hashed = user_password
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