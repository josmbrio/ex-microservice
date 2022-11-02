from flask import Blueprint, request, jsonify
from json_web_token import create_token, check_token

authorization = Blueprint('route_token', __name__)


@authorization.route('/auth', methods=['POST'])
def auth():
    username = request.json['username']
    password = request.json['password']
    if username == 'ex-user' and password == 'pa55w0rd':
        token = create_token(values=request.json)
        return token
    else:
        response = jsonify({"message": "Bad credentials"})
        response.status_code = 404
        return response


@authorization.route('/verify')
def verify_token():
    token = request.json['Authorization']
    return check_token(token)