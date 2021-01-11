from RestfulRegistration.api.api import api
from flask_restplus import Resource
from flask import request, jsonify, make_response
import firebase_admin
from firebase_admin import credentials, firestore
from RestfulRegistration.api.implementation import get_users_list, create_user, get_user, update_user, delete_user

namespace = api.namespace('users', description='Operations on user resources')

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