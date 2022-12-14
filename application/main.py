from flask import Flask, jsonify
from routes.endpoints import info
from routes.token import authorization
from flask_jwt_extended import JWTManager
from datetime import timedelta
from redis_connection.redis_connection import jwt_redis_denylist

application = Flask(__name__)

application.config["JWT_SECRET_KEY"] = "xxlpirqixmes"
application.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=1)
application.config["JWT_HEADER_NAME"] = 'X-JWT-KWY'
application.config["JWT_HEADER_TYPE"] = ""

jwt = JWTManager(application)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_denylist.get(jti)
    return token_in_redis is not None


application.register_blueprint(authorization)
application.register_blueprint(info)


@application.errorhandler(405)
def error_405(error=None):
    response = jsonify({"message": "ERROR"})
    response.status_code = 405
    return response


@application.errorhandler(404)
def error_404(error=None):
    response = jsonify({"message": "ERROR"})
    response.status_code = 404
    return response


if __name__ == '__main__':
    application.run(debug=True, port=9000, host='0.0.0.0')