from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token

authorization = Blueprint('route_token', __name__)


@authorization.route('/auth', methods=['POST'])
def auth_token():
    token = create_access_token(identity="ex-user")
    return jsonify(token=token)
