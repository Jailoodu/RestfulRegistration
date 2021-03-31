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
    expected_data = [{"address":{"city":"Ottoport","country":"United States of America","state":"Ohio","street":"73671 Lindgren Street","zipCode":"32282"},"age":21,"email":"Kevin_Lind@yahoo.com","id":"cb144b51-0b9e-45b7-bb38-0e4cddee2827","name":"Marsha Price","phone":"399-731-2777 x25031","status":"Confirmed"},
    {"address":{"city":"West Alexandrine","country":"United States of America","state":"Nevada","street":"50567 Kub Lodge","zipCode":"38255"},"age":28,"email":"Franco81@hotmail.com","id":"7e2561ab-00c9-4b14-abad-f58d337690ec","name":"Ora Steuber","phone":"655-637-2850 x6495","status":"Confirmed"},
    {"address":{"city":"Wehnerland","country":"United States of America","state":"Vermont","street":"45594 Violet Forge","zipCode":"70718"},"age":19,"email":"Katlynn39@gmail.com","id":"54a05019-6433-43e6-8efc-a1d05f457973","name":"Tracey Kassulke","phone":"212.606.2391 x2282","status":"Accepted"}]
    # Use a test client configured for testing
    with flask_app.test_client() as test_client:
        for i in range(NUM):
            print("Running GET /users/user_id stress test: iteration #{}".format(i),file=sys.stderr)
            user = random.choice(expected_data)
            response = test_client.get('/api/users/{}'.format(user["id"]))
            assert response.status_code == 200
            assert response.status == "200 OK"
            
            data = response.get_json()
            assert user == data

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