from api.api import api
from flask_restplus import Resource, fields
from flask import request, jsonify, make_response, Response
import firebase_admin
from firebase_admin import credentials, firestore
from api.implementation import get_users_list, create_user, get_user, update_user, delete_user, normalize, make_payment, send_email

# namespace sets the endpoints with a prefix of /users
namespace = api.namespace('users', description='Operations on user resources')

# Models
user_model = namespace.model(
    "User",
    {
        "any": fields.String(description="Any user fields you need"),
    },
)

@namespace.route('/') 
class UserCollection(Resource):
    @api.doc(responses = {200: 'OK', 500: 'Error fetching data' })
    def get(self):
        """
        Returns all of the users in the database
        """
        l = get_users_list()
        resp = make_response(jsonify(l), 200)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    
    @api.doc(responses = {201: 'User successfully created', 400: 'Error occurred' })
    @namespace.expect(user_model)
    def post(self):
        """
        Create a new user
        """
        create_user(request.json)
        resp = make_response('', 201)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

@namespace.route('/<string:user_id>')
class User(Resource):
    @api.doc(responses = { 200: 'OK', 404: 'Error occurred: User not found' })
    def get(self, user_id):
        """
        Return a user with the specified ID
        """
        user_data = get_user(user_id)
        if user_data:
            resp = make_response(jsonify(user_data), 200)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
        else:
            return None, 404
    
    @api.doc(responses = { 204: 'User fields updated', 500: 'Error occurred' })
    @namespace.expect(user_model)
    def put(self, user_id):
        """
        Update fields for a specified user
        """
        update_user(request.json, user_id)
        resp = make_response('', 204)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    
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

# namespace sets the endpoints with a prefix of /payments
paymentNamespace = api.namespace('payments', description='Operations on payment resources')

# Models
payment_model = namespace.model(
    "Payment",
    {
        "cardNumber": fields.String(description="Credit card number"),
        "expirationDate": fields.String(description="Credit card expiration date"),
        "amount": fields.String(description="Dollar amount"),
        "email": fields.String(description="Email to send confirmation")
    },
)

@paymentNamespace.route('/') 
class PaymentCollection(Resource):
    @api.doc(responses = {201: 'Payment successfully completed', 400: 'Error occurred' })
    @paymentNamespace.expect(payment_model)
    def post(self):
        """
        Pay event organizers
        """
        rc = make_payment(request.json)
        if rc == 0:
            send_email(request.json) 
            return None, 201
        else:
            return None, 400 