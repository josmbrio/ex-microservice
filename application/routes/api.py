from datetime import timedelta
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from redis_connection.redis_connection import jwt_redis_denylist


info = Blueprint('info', __name__)


@info.route('/DevOps', methods=['POST'])
@jwt_required()
def get_info():
    api_key = '2f5ae96c-b558-4c7b-a590-a501ae1c3f6c'
    request_api_key = request.headers.get('X-Parse-REST-API-Key')
    if request_api_key == api_key:
        var_to = request.json['to']
        jti = get_jwt()["jti"]
        jwt_redis_denylist.set(jti, "", ex=timedelta(minutes=1))
        return jsonify({"message": "Hello " + var_to + " your message will be send"})
    else:
        return jsonify({"message": "Incorrect API KEY"})


@info.errorhandler(405)
def error_405(error=None):
    response = jsonify({"message": "ERROR"})
    response.status_code = 405
    return response


@info.errorhandler(404)
def error_404(error=None):
    response = jsonify({"message": "ERROR"})
    response.status_code = 404
    return response

