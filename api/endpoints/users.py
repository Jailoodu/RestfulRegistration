from api.api import api
from flask_restplus import Resource
from flask import request, jsonify, make_response, Response
import firebase_admin
from firebase_admin import credentials, firestore
from api.implementation import get_users_list, create_user, get_user, update_user, delete_user, normalize

# namespace sets the endpoints with a prefix of /users
namespace = api.namespace('users', description='Operations on user resources')

@namespace.route('/') 
class UserCollection(Resource):
    @api.doc(responses = {200: 'OK', 500: 'Error fetching data' })
    def get(self):
        """
        Returns all of the users in the database
        """
        l = get_users_list()
        return make_response(jsonify(l), 200)
    
    @api.doc(responses = {201: 'User successfully created', 400: 'Error occurred' })
    def post(self):
        """
        Create a new user
        """
        create_user(request.json)
        return None, 201

@namespace.route('/<string:user_id>')
class User(Resource):
    @api.doc(responses = { 200: 'OK', 404: 'Error occurred' })
    def get(self, user_id):
        """
        Return a user with the specified ID
        """
        user_data = get_user(user_id)
        if user_data:
            return make_response(jsonify(user_data), 200)
        else:
            return None, 404
    
    @api.doc(responses = { 204: 'User fields updated', 500: 'Error occurred' })
    def put(self, user_id):
        """
        Update fields for a specified user
        """
        update_user(request.json, user_id)
        return None, 204
    
    @api.doc(responses = { 202: 'User deleted', 500: 'Error occurred' })
    def delete(self, user_id):
        """
        Delete a user with the specified ID
        """
        delete_user(user_id)
        return None, 202

@namespace.route('/file')
class File(Resource):
    @api.doc(responses = { 200: 'OK', 500: 'Error occurred' })
    def get(self):
        """
        Return a csv file with all of the users
        """
        l = get_users_list()
        updated_list = normalize(l)
        resp = make_response(updated_list.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=export.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp