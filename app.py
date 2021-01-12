import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask, Blueprint
from RestfulRegistration.api.endpoints.users import namespace as ns
from RestfulRegistration.api.api import api

# initialize a Flash (WSGI) application
app = Flask(__name__)

def start_app(app):
    # the endpoint will be hostname:port/api
    bp = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(bp)
    api.add_namespace(ns)
    # blueprint helps organize a group of related views
    app.register_blueprint(bp)

def main():
    start_app(app)
    app.run()

# main function is automatically run
if __name__ == '__main__':
    main()