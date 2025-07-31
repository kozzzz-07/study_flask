from unittest.mock import patch
from domain.user_domain import User
from services.user_service import UserService
from application.ports.user_dto import UserResponse, UserCreateDTO


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
    with patch("services.user_service.IUserRepository") as MockUserRepository:
        # モックの設定: get_usersが呼ばれたらダミーデータを返すようにする
        MockUserRepository.return_value.get_users.return_value = mock_domain_users

        # テスト対象のクラスとメソッドを呼び出す
        user_service = UserService(MockUserRepository.return_value)
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


def test_add_user_with_mock():
    """UserRepositoryをモック化してUserServiceのadd_userをテストする"""
    # 1. Arrange: テストの準備
    user_create_dto = UserCreateDTO(name="New User", age=28, nickname="Newbie")
    # add_userが返すダミーのドメインモデルを作成（IDはリポジトリが割り当てる想定）
    mock_created_domain_user = User(id=3, name="New User", age=28, nickname="Newbie")

    # 2. Act: テスト対象の処理を実行
    with patch("services.user_service.IUserRepository") as MockUserRepository:
        # モックの設定: add_userが呼ばれたらダミーデータを返すようにする
        MockUserRepository.return_value.add_user.return_value = mock_created_domain_user

        # テスト対象のクラスとメソッドを呼び出す
        user_service = UserService(MockUserRepository.return_value)
        result_dto = user_service.add_user(user_create_dto)

    # 3. Assert: 結果の検証
    # モックが正しく呼び出されたか
    MockUserRepository.return_value.add_user.assert_called_once()
    # add_userがUserドメインモデルで呼ばれたことを確認
    called_with_user = MockUserRepository.return_value.add_user.call_args[0][0]
    assert isinstance(called_with_user, User)
    assert called_with_user.name == user_create_dto.name
    assert called_with_user.age == user_create_dto.age
    assert called_with_user.nickname == user_create_dto.nickname
    assert called_with_user.id is None # サービス層からリポジトリに渡す時点ではIDはNone

    # 戻り値がUserResponse DTOであるか
    assert isinstance(result_dto, UserResponse)
    # DTOの内容が正しく変換されているか
    assert result_dto.id == mock_created_domain_user.id
    assert result_dto.name == mock_created_domain_user.name
    assert result_dto.age == mock_created_domain_user.age
    assert result_dto.nickname == mock_created_domain_user.nickname
