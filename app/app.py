import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask, Blueprint
from api.endpoints.users import namespace as ns
from api.api import api
from flask_cors import CORS
from dotenv import load_dotenv

# initialize a Flash (WSGI) application
app = Flask(__name__)
cors = CORS(app, resources={r'/*': {'origins': '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'

bp = Blueprint('api', __name__, url_prefix='/api')

def start_app(app):
    # the endpoint will be hostname:port/api
    api.init_app(bp)
    api.add_namespace(ns)
    # blueprint helps organize a group of related views
    app.register_blueprint(bp)

def main():
    load_dotenv()
    start_app(app)
    app.run(host ='0.0.0.0', port = 5001)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

# main function is automatically run
if __name__ == '__main__':
    main()