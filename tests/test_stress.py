import pytest
from flask import json
from tests.test_utils import cleanup, setup_env
from api.implementation import get_firestore_id
from tests.test_app import flask_app
from app.app import app
import sys
import random

"""
IMPORTANT NOTICE: Currently for each stress test, the endpoints are called NUM times. As NUM increases, the endpoint will be called more often for the specific test. 
Due to daily quota limitations provided by Google Cloud Platform, I have set NUM = 2. If the daily quota is passed, the API will not be able to function appropriately.
"""
NUM = 1

def test_stress_get_users():
    """
    GET /users/
    """
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        for i in range(NUM):
            print("Running GET /users/ stress test: iteration #{}".format(i),file=sys.stderr)
            response = test_client.get('/api/users/')
            assert response.status_code == 200
            assert response.status == "200 OK"
            data = response.get_json()
            assert len(data) > 0 

def test_stress_get_user_details():
    """
    GET /users/{user_id}
    """
    expected_data = [{"id":"fd7207c0-c7a4-47fa-b750-a9abd9d1b9d9", "status":"Accepted"}, {"id":"52366687-c844-4b40-be72-482a65e6ef0b", "status":"Pending"}, {"id":"f3006864-8a5a-41cf-90ab-08b220687a78", "status":"Pending"}, {"id":"7cef8d54-ee81-4220-ad73-ef5c82f6e45e", "status":"Pending"}]
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        for i in range(NUM):
            print("Running GET /users/user_id stress test: iteration #{}".format(i),file=sys.stderr)
            user = random.choice(expected_data)
            response = test_client.get('/api/users/{}'.format(user["id"]))
            assert response.status_code == 200
            assert response.status == "200 OK"
            
            data = response.get_json()
            assert user["id"] == data["id"]
            assert user["status"] == data["status"]

def test_stress_retrieve_file():
    """
    GET /users/file
    """
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        for i in range(NUM):
            print("Running GET /users/file stress test: iteration #{}".format(i),file=sys.stderr)
            response = test_client.get('/api/users/file')
            assert response.status_code == 200
            assert response.status == "200 OK"
            
            header = response.headers
            assert header.get("Content-Disposition") == "attachment; filename=export.csv"
            assert header.get("Content-Type") == "text/csv"

def test_stress_create_user():
    """
    POST /users/
    """
    users = [{"name": "Saj Diesel", "age": 54},{"name": "Dominic Cruz", "age": 29},
    {"name": "Alicia Sousa", "age": 22},{"name": "Jacob Wright", "age": 36},
    {"name": "Lillian Angie", "age": 43},{"name": "Celest Hainge", "age": 31}]
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        for i in range(NUM):
            created_user = random.choice(users)
            response = test_client.post('/api/users/', json={
                "name": created_user["name"], "age": created_user["age"]
            })
            assert response.status_code == 201
            assert response.status == "201 CREATED"
            uid_body = response.get_json()

            endpoint = '/api/users/{}'.format(uid_body["id"])
            response = test_client.get(endpoint)
            assert response.status_code == 200
            assert response.status == "200 OK"
            
            data = response.get_json()
            assert data['name'] == created_user['name']
            assert data['age'] == created_user['age']
            assert data['status'] == "Pending"
            assert data['id'] == uid_body['id']

            cleanup(test_client, uid_body["id"]) 

def test_stress_delete_user():
    """
    DELETE /users/{user_id}
    """
    created_user = {"name": "Gabriel Romel", "age":32}
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        for i in range(NUM):
            print("Running DELETE /users/user_id stress test: iteration #{}".format(i),file=sys.stderr)
            resp_body = setup_env(test_client, created_user)
            endpoint = '/api/users/{}'.format(resp_body["id"])
            response = test_client.delete(endpoint)
            assert response.status_code == 202
            assert response.status == "202 ACCEPTED"

            response = test_client.get(endpoint)
            assert response.status_code == 404
            assert response.status == "404 NOT FOUND"

def test_stress_update_user():
    """
    PUT /users/{user_id}
    """
    created_user = {"name": "James Han", "age":38}
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        for i in range(NUM):
            print("Running PUT /users/user_id stress test: iteration #{}".format(i),file=sys.stderr)
            resp_body = setup_env(test_client, created_user)
            endpoint = '/api/users/{}'.format(resp_body["id"])
            response = test_client.put(endpoint, json={
                "status": "Accepted"
            })
            assert response.status_code == 204
            assert response.status == "204 NO CONTENT"

            response = test_client.get(endpoint)
            assert response.status_code == 200
            assert response.status == "200 OK"
            
            data = response.get_json()
            assert data["id"] == resp_body["id"]
            assert data["name"] == created_user["name"]
            assert data["age"] == created_user["age"]

            cleanup(test_client, resp_body["id"])