from flask import Blueprint, request, jsonify
from json_web_token import check_token

info = Blueprint('info', __name__)


@info.before_request
def validate_jwt():
    token = request.headers.get('X-JWT-KWY')
    print(token)
    return check_token(token)


@info.route('/DevOps', methods=['POST'])
def get_info():
    print(request.json)
    api_key = '2f5ae96c-b558-4c7b-a590-a501ae1c3f6c'
    try:
        request_api_key = request.headers.get('X-Parse-REST-API-Key')
        print(request_api_key)
        if request_api_key == api_key:
            var_to = request.json['to']
            return jsonify({"message": "Hello " + var_to + " your message will be send"})
        else:
            return jsonify({"message": "Incorrect API KEY"})
    except KeyError:
        return jsonify({"message": "You must defined the key X-Parse-REST-API-Key"})


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

