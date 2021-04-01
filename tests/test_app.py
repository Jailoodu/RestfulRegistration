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
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/api/users/fd7207c0-c7a4-47fa-b750-a9abd9d1b9d9')
        assert response.status_code == 200
        assert response.status == "200 OK"
        
        data = response.get_json()
        assert data["id"] == "fd7207c0-c7a4-47fa-b750-a9abd9d1b9d9"
        assert data["status"] == "Accepted"

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
    created_user = {"name": "Jacob Wright", "age": 25}
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.post('/api/users/', json={
            "name": created_user["name"]
        })
        assert response.status_code == 201
        assert response.status == "201 CREATED"
        resp_body = response.get_json()

        endpoint = '/api/users/{}'.format(resp_body["id"])
        response = test_client.get(endpoint)
        assert response.status_code == 200
        assert response.status == "200 OK"
        
        data = response.get_json()
        assert data["name"] == created_user["name"]
        assert data["status"] == "Pending"

        cleanup(test_client, resp_body["id"]) 

def test_delete_user():
    """
    DELETE /users/{user_id}
    Requirements: F-1
    """
    created_user = {"name": "John Brown", "age": 23}
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        uid_body = setup_env(test_client, created_user)
        endpoint = '/api/users/{}'.format(uid_body["id"])
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
    created_user = {"name": "Robert Langdon", "age":55}
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        uid_body = setup_env(test_client, created_user)
        endpoint = '/api/users/{}'.format(uid_body["id"])
        response = test_client.put(endpoint, json={
            "status": "Confirmed"
        })
        assert response.status_code == 204
        assert response.status == "204 NO CONTENT"

        response = test_client.get(endpoint)
        assert response.status_code == 200
        assert response.status == "200 OK"
        
        data = response.get_json()
        assert data["name"] == created_user["name"]
        assert data["age"] == created_user["age"]
        assert data["status"] == "Confirmed"
        assert data["id"] == uid_body["id"]

        cleanup(test_client, uid_body["id"])

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

def test_make_payment():
    """
    POST /users/{user_id}/payment
    Requirements: F-36
    """
    with flask_app.test_client() as test_client:
        response = test_client.post('/api/payments', json={"cardNumber": "370000000000002","expirationDate": "2020-12","cardCode": "6543","amount": "23.99","email": "jason.loodu@gmail.com"})
        assert response.status_code == 308

def test_make_payment_negative_fail():
    """
    POST /users/{user_id}/payment
    Requirements: F-36
    """
    with flask_app.test_client() as test_client:
        response = test_client.post('/api/users/76fbjs-43ff-9j8f/payment', json={})
        assert response.status_code == 404
        assert response.status == "404 NOT FOUND"