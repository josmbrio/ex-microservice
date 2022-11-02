from dotenv import load_dotenv
from flask import Flask, jsonify, request, Response
from routes.api import info
from routes.token import authorization

application = Flask(__name__)

application.register_blueprint(authorization)
application.register_blueprint(info)


if __name__ == '__main__':
    load_dotenv()
    application.run(debug=True,port='5000',host='localhost')