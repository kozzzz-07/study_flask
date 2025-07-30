from application.ports.user_dto import UserResponse
from application.ports.user_repository_port import IUserRepository


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get_users(self) -> list[UserResponse]:
        users = self.user_repository.get_users()
        # ドメインモデルからDTOへの変換
        return [UserResponse.model_validate(user.model_dump()) for user in users]
