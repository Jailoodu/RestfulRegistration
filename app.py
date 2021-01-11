import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask, Blueprint
from flask_restplus import Resource, Api
from flask import request, jsonify, make_response
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)
api = Api(version='1.0', title='Registration API',
          description='An API which allows interactivity with users')

namespace = api.namespace('users', description='Operations on user resources')


cred = credentials.Certificate("serviceAccount.json")
firebase_admin.initialize_app(cred)
firestore_db = firestore.client()

@namespace.route('/') 
class UserCollection(Resource):
    def get(self):
        """
        Returns a list of users
        """
        l = get_users_list()
        return make_response(jsonify(l), 200)
    
    @api.response(201, "User successfully created")
    def post(self):
        """
        Create a new user
        """
        create_user(request.json)
        return None, 201

@namespace.route('/<string:user_id>')
class User(Resource):
    def get(self, user_id):
        """
        Return a specified user
        """
        user_data = get_user(user_id)
        if user_data:
            return make_response(jsonify(user_data), 200)
        else:
            return None, 404
    
    def put(self, user_id):
        """
        Update fields for a specified user
        """
        update_user(request.json, user_id)
        return None, 204
    
    def delete(self, user_id):
        """
        Delete a specified user
        """
        delete_user(user_id)
        return None, 202


def get_users_list():
    snapshots = list(firestore_db.collection(u'users').get())
    li = []
    for snapshot in snapshots:
        li.append(snapshot.to_dict())
    return li

def create_user(data):
    firestore_db.collection(u'users').add(data)

def get_user(id):
    users_ref = firestore_db.collection(u'users')
    query = users_ref.where(u'id', u'==', id)
    docs = query.get()
    if len(docs) > 0:
        for doc in docs:
            return doc.to_dict()
    else:
        return None

def update_user(data, id):
    users_ref = firestore_db.collection(u'users')
    query = users_ref.where(u'id', u'==', id)
    docs = query.get()
    doc_id = docs[0].id

    user_ref = firestore_db.collection(u'users').document(doc_id)
    user_ref.update(data)

def delete_user(id):
    users_ref = firestore_db.collection(u'users')
    query = users_ref.where(u'id', u'==', id)
    docs = query.get()
    doc_id = docs[0].id

    user_ref = firestore_db.collection(u'users').document(doc_id)
    user_ref.delete()

def start_app(app):
    bp = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(bp)
    api.add_namespace(namespace)
    app.register_blueprint(bp)

def main():
    start_app(app)
    app.run()

if __name__ == '__main__':
    main()