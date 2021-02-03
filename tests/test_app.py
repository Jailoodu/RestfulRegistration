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
    """
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/api/users/')
        assert response.status_code == 200
        assert response.status == "200 OK"

def test_get_user_details():
    """
    GET /users/{user_id}
    """
    expected_data = {"name":"Tammy Stracke","phone":"813-590-8730 x62243", "status":"Pending", "address":{"city":"Jailynberg","country":"United States of America","state":"Tennessee","street":"570 Delmer Key","zipCode":"77974-5063"}, "age":50, "email":"Carli.Waelchi56@hotmail.com", "id":"85645cbb-58dd-40cd-b74c-8881783a49a8"}
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/api/users/85645cbb-58dd-40cd-b74c-8881783a49a8')
        assert response.status_code == 200
        assert response.status == "200 OK"
        
        data = response.get_json()
        assert expected_data == data

def test_create_user():
    """
    POST /users/
    """
    created_user = {"name": "Jacob Wright", "status": "Confirmed", "id": "1234567890abc"}
    # Create a test client using the Flask application configured for testing
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
    """
    created_user = {"name": "Jacob Wright", "status": "Confirmed", "id": "1234567890abc"}
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        setup_env(test_client, created_user)
        endpoint = '/api/users/{}'.format(created_user["id"])
        response = test_client.delete(endpoint)
        assert response.status_code == 202
        assert response.status == "202 ACCEPTED"

        response = test_client.get(endpoint)
        assert response.status_code == 404

def test_update_user():
    """
    PUT /users/{user_id}
    """
    created_user = {"name": "Jacob Wright", "status": "Accepted", "id": "1234567890abc"}
    # Create a test client using the Flask application configured for testing
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

def test_retrieve_file():
    """
    GET /users/file
    """
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/api/users/file')
        assert response.status_code == 200
        assert response.status == "200 OK"
        
        header = response.headers
        assert header.get("Content-Disposition") == "attachment; filename=export.csv"
        assert header.get("Content-Type") == "text/csv"