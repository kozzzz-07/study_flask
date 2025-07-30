import pytest
from flask import Flask
from unittest.mock import MagicMock, patch
from route.user import user_bp
from services.user_service import UserService

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    with app.test_client() as client:
        yield client

def test_get_users(client):
    mock_users = [
        {"id": 1, "name": "John Doe", "age": 30, "nickname": None},
        {"id": 2, "name": "Jane Smith", "age": 25, "nickname": "Janey"}
    ]
    with patch('route.user.UserService') as MockUserService:
        MockUserService.return_value.get_users.return_value = mock_users
        response = client.get('/users')
        assert response.status_code == 200
        assert response.json == mock_users
