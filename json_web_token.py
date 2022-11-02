from jwt import encode, decode
from flask import jsonify
from os import getenv
from datetime import datetime, timedelta
from jwt import exceptions



def expiration_date(days: int):
    return datetime.now() + timedelta(days)


def create_token(values: dict):
    token = encode(payload={**values, "exp": expiration_date(1)}, key=getenv('KEY_SECRET'))
    return token.encode('UTF-8')


def check_token(token):
    try:
        decode(token, key=getenv('KEY_SECRET'), algorithms=['HS256'])
    except exceptions.DecodeError:
        response = jsonify({"message" : "Invalid token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"message" : "Expired token"})
        response.status_code = 401
        return response

