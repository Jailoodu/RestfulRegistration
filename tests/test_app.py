import pytest
from flask import json
from app.app import app, start_app
from tests.test_utils import cleanup, setup_env
from api.implementation import get_firestore_id

flask_app = app
start_app(flask_app)

def test_get_users():
    """
    GET /users/
    Requirements: F-1
    """
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/api/users/')
        assert response.status_code == 200
        assert response.status == "200 OK"
        data = response.get_json()
        assert len(data) > 0

def test_get_user_details():
    """
    GET /users/{user_id}
    Requirements: F-1
    """
    expected_data = {
        "address":{
            "city":"Dwightmouth",
            "country":"United States of America",
            "state":"South Carolina",
            "street":"736 Torphy Trail",
            "zipCode":"91907-4722"
        },
        "age":43,
        "email":"Ricardo_Parker21@yahoo.com",
        "id":"f9cc624e-0a2f-40fa-bd36-7c291f9c93d7",
        "name":"Jeannette Olson III",
        "phone":"(764) 834-2840 x618",
        "status":"Rejected"
    }
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/api/users/f9cc624e-0a2f-40fa-bd36-7c291f9c93d7')
        assert response.status_code == 200
        assert response.status == "200 OK"
        
        data = response.get_json()
        assert expected_data == data

def test_get_user_details_negative():
    """
    GET /users/{user_id}
    Requirements: F-1
    """
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/api/users/98645db-58dd-83jh-b74c-887a8')
        assert response.status_code == 404
        assert response.status == "404 NOT FOUND"

def test_create_user():
    """
    POST /users/
    Requirements: F-1
    """
    created_user = {"name": "Jacob Wright", "status": "Confirmed", "id": "1234567890abc"}
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.post('/api/users/', json={
            "name": created_user["name"], "status": created_user["status"], "id": created_user["id"]
        })
        assert response.status_code == 201
        assert response.status == "201 CREATED"

        endpoint = '/api/users/{}'.format(created_user["id"])
        response = test_client.get(endpoint)
        assert response.status_code == 200
        assert response.status == "200 OK"
        
        data = response.get_json()
        assert data == created_user

        cleanup(test_client, created_user["id"]) 

def test_delete_user():
    """
    DELETE /users/{user_id}
    Requirements: F-1
    """
    created_user = {"name": "Jacob Wright", "status": "Confirmed", "id": "1234567890abc"}
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        setup_env(test_client, created_user)
        endpoint = '/api/users/{}'.format(created_user["id"])
        response = test_client.delete(endpoint)
        assert response.status_code == 202
        assert response.status == "202 ACCEPTED"

        response = test_client.get(endpoint)
        assert response.status_code == 404
        assert response.status == "404 NOT FOUND"

def test_delete_user_negative():
    """
    DELETE /users/{user_id}
    Requirements: F-1
    """
    created_user = {"name": "Daniel Snod", "status": "Confirmed", "id": "3g42j3743jj"}
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        endpoint = '/api/users/{}'.format(created_user["id"])
        response = test_client.delete(endpoint)
        assert response.status_code == 500
        assert response.status == "500 INTERNAL SERVER ERROR"

        response = test_client.get(endpoint)
        assert response.status_code == 404
        assert response.status == "404 NOT FOUND"

def test_update_user():
    """
    PUT /users/{user_id}
    Requirements: F-21
    """
    created_user = {"name": "Jacob Wright", "status": "Accepted", "id": "1234567890abc"}
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        setup_env(test_client, created_user)
        endpoint = '/api/users/{}'.format(created_user["id"])
        response = test_client.put(endpoint, json={
            "status": "Confirmed"
        })
        assert response.status_code == 204
        assert response.status == "204 NO CONTENT"

        response = test_client.get(endpoint)
        assert response.status_code == 200
        assert response.status == "200 OK"
        
        data = response.get_json()
        expected_user = {"name": "Jacob Wright", "status": "Confirmed", "id": "1234567890abc"}
        assert data == expected_user

        cleanup(test_client, created_user["id"])

def test_update_user_negative():
    """
    PUT /users/{user_id}
    Requirements: F-21
    """
    created_user = {"name": "Haley King", "status": "Confirmed", "id": "76348264ghdas"}
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        endpoint = '/api/users/{}'.format(created_user["id"])
        response = test_client.put(endpoint, json={
            "status": "Confirmed"
        })
        assert response.status_code == 500
        assert response.status == "500 INTERNAL SERVER ERROR"

        response = test_client.get(endpoint)
        assert response.status_code == 404
        assert response.status == "404 NOT FOUND"

def test_retrieve_file():
    """
    GET /users/file
    Requirements: F-38
    """
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/api/users/file')
        assert response.status_code == 200
        assert response.status == "200 OK"
        
        header = response.headers
        assert header.get("Content-Disposition") == "attachment; filename=export.csv"
        assert header.get("Content-Type") == "text/csv"

# Tests for endpoints that are still to be implemented
def test_get_payment_details_fail():
    """
    GET /users/{user_id}/payment
    Requirements: F-36
    """
    with flask_app.test_client() as test_client:
        response = test_client.get('/api/users/85645cbb-58dd-40cd-b74c-8881783a49a8/payment')
        assert response.status_code == 200
        assert response.status == "200 OK"

def test_get_payment_details_negative_fail():
    """
    GET /users/{user_id}/payment
    Requirements: F-36
    """
    with flask_app.test_client() as test_client:
        response = test_client.get('/api/users/894hjd-53da-76gh-bc-87fdsa3/payment')
        assert response.status_code == 404
        assert response.status == "404 NOT FOUND"

def test_make_payment_fail():
    """
    POST /users/{user_id}/payment
    Requirements: F-36
    """
    with flask_app.test_client() as test_client:
        response = test_client.post('/api/users/85645cbb-58dd-40cd-b74c-8881783a49a8/payment', json={})
        assert response.status_code == 201
        assert response.status == "201 CREATED"

def test_make_payment_negative_fail():
    """
    POST /users/{user_id}/payment
    Requirements: F-36
    """
    with flask_app.test_client() as test_client:
        response = test_client.post('/api/users/76fbjs-43ff-9j8f/payment', json={})
        assert response.status_code == 404
        assert response.status == "404 NOT FOUND"