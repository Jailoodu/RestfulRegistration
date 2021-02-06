import pytest
from flask import json
from tests.test_utils import cleanup, setup_env
from api.implementation import get_firestore_id
from tests.test_app import flask_app
from app.app import app
import sys

def test_stress_get_users():
    """
    GET /users/
    """
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        for i in range(5):
            print("Running GET /users/ stress test: iteration #{}".format(i),file=sys.stderr)
            response = test_client.get('/api/users/')
            assert response.status_code == 200
            assert response.status == "200 OK"
            data = response.get_json()
            assert len(data) > 0

def test_stress_retrieve_file():
    """
    GET /users/file
    """
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        for i in range(5):
            print("Running GET /users/file stress test: iteration #{}".format(i),file=sys.stderr)
            response = test_client.get('/api/users/file')
            assert response.status_code == 200
            assert response.status == "200 OK"
            
            header = response.headers
            assert header.get("Content-Disposition") == "attachment; filename=export.csv"
            assert header.get("Content-Type") == "text/csv"