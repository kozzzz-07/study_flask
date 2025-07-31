import pytest
from flask import Flask
from unittest.mock import patch
from route.user import user_bp
from application.ports.user_dto import UserResponse, UserCreateDTO  # DTOをインポート


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


def test_add_user(client):
    user_data = {"name": "New User", "age": 28, "nickname": "Newbie"}
    expected_response_dto = UserResponse(id=3, name="New User", age=28, nickname="Newbie")

    with patch('route.user.get_user_service') as MockGetUserService:
        mock_user_service_instance = MockGetUserService.return_value
        mock_user_service_instance.add_user.return_value = expected_response_dto

        response = client.post('/users', json=user_data)

        assert response.status_code == 201
        assert response.json == expected_response_dto.model_dump()
        mock_user_service_instance.add_user.assert_called_once()
        # add_userがUserCreateDTOで呼ばれたことを確認
        called_with_dto = mock_user_service_instance.add_user.call_args[0][0]
        assert isinstance(called_with_dto, UserCreateDTO)
        assert called_with_dto.name == user_data["name"]
        assert called_with_dto.age == user_data["age"]
        assert called_with_dto.nickname == user_data["nickname"]
