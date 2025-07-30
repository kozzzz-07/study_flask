import pytest
from flask import Flask
from unittest.mock import patch
from route.user import user_bp
from domain.user_domain import User


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    with app.test_client() as client:
        yield client


def test_get_users(client):
    # Userモデルのインスタンスを作成
    mock_users_data = [
        User(id=1, name="John Doe", age=30, nickname=None),
        User(id=2, name="Jane Smith", age=25, nickname="Janey"),
    ]
    # レスポンスの期待値（JSONになるデータ）
    expected_json = [
        {"id": 1, "name": "John Doe", "age": 30, "nickname": None},
        {"id": 2, "name": "Jane Smith", "age": 25, "nickname": "Janey"},
    ]

    with patch("route.user.UserService") as MockUserService:
        # モックはUserモデルのリストを返すように設定
        MockUserService.return_value.get_users.return_value = mock_users_data
        response = client.get("/users")

        assert response.status_code == 200
        assert response.json == expected_json
