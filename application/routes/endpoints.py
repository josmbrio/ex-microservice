from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from redis_connection.redis_connection import add_jwt_to_denylist
from util_functions.api_key_validation import is_valid_api_key


info = Blueprint('info', __name__)


@info.route('/DevOps', methods=['POST'])
@jwt_required()
def get_info():
    request_api_key = request.headers.get('X-Parse-REST-API-Key')
    if is_valid_api_key(request_api_key):
        received_payload = request.json
        if "to" in received_payload:
            add_jwt_to_denylist()
            var_to = request.json['to']
            return jsonify({"message": "Hello " + var_to + " your message will be send"})
        else:
            return jsonify({"message": "Invalid payload"})
    else:
        return jsonify({"message": "Incorrect API KEY"})


@info.route('/health', methods=['GET'])
def get_health():
    return jsonify({"message": "OK"})


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

