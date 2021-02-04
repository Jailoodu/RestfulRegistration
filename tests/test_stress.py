from tests.test_app import flask_app
from tests.test_utils import cleanup, setup_env

def test_create_user():
    """
    POST /users/
    """
    created_user = {"name": "Jacob Wright", "status": "Confirmed", "id": "1234567890abc"}
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        for _ in range(101):
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