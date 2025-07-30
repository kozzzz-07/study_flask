from application.ports.user_dto import UserResponse
from infra.repository.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_users(self) -> list[UserResponse]:
        users = self.user_repository.get_users()
        # ドメインモデルからDTOへの変換
        return [UserResponse.model_validate(user.model_dump()) for user in users]
        