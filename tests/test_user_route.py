import pytest
from flask import Flask
from unittest.mock import patch
from route.user import user_bp
from application.ports.user_dto import UserResponse  # DTOをインポート


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(user_bp)
    with app.test_client() as client:
        yield client


def test_get_users(client):
    # UserServiceが返すダミーのDTOリストを作成
    mock_dtos = [
        UserResponse(id=1, name="DTO User 1", age=30, nickname="Dto1"),
        UserResponse(id=2, name="DTO User 2", age=25, nickname="Dto2"),
    ]
    # レスポンスの期待値（JSONになるデータ）
    expected_json = [
        {"id": 1, "name": "DTO User 1", "age": 30, "nickname": "Dto1"},
        {"id": 2, "name": "DTO User 2", "age": 25, "nickname": "Dto2"},
    ]

    with patch('route.user.get_user_service') as MockGetUserService:
        # get_user_serviceが返すモックのUserServiceインスタンスを作成
        mock_user_service_instance = MockGetUserService.return_value
        # そのモックインスタンスのget_usersメソッドがDTOのリストを返すように設定
        mock_user_service_instance.get_users.return_value = mock_dtos
        response = client.get('/users')

        assert response.status_code == 200
        assert response.json == expected_json
