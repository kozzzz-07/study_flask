from unittest.mock import patch
from domain.user_domain import User
from services.user_service import UserService
from application.ports.user_dto import UserResponse


def test_get_users_with_mock():
    """UserRepositoryをモック化してUserServiceをテストする"""
    # 1. Arrange: テストの準備
    # UserRepositoryが返すダミーのドメインモデルリストを作成
    mock_domain_users = [
        User(id=1, name="Domain User 1", age=30, nickname="Dom1"),
        User(id=2, name="Domain User 2", age=25, nickname="Dom2"),
    ]

    # 2. Act: テスト対象の処理を実行
    # `services.user_service.UserRepository` をモックに差し替える
    with patch("services.user_service.UserRepository") as MockUserRepository:
        # モックの設定: get_usersが呼ばれたらダミーデータを返すようにする
        MockUserRepository.return_value.get_users.return_value = mock_domain_users

        # テスト対象のクラスとメソッドを呼び出す
        user_service = UserService()
        result_dtos = user_service.get_users()

    # 3. Assert: 結果の検証
    # モックが正しく呼び出されたか
    MockUserRepository.return_value.get_users.assert_called_once()

    # 戻り値がDTOのリストであるか
    assert isinstance(result_dtos, list)
    assert len(result_dtos) == 2
    assert all(isinstance(dto, UserResponse) for dto in result_dtos)

    # DTOの内容がドメインモデルから正しく変換されているか
    assert result_dtos[0].id == mock_domain_users[0].id
    assert result_dtos[0].name == mock_domain_users[0].name
    assert result_dtos[1].age == mock_domain_users[1].age
