from application.ports.user_dto import UserResponse
from application.ports.user_repository_port import IUserRepository
from utils.logging import get_logger


logger = get_logger(__name__)


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get_users(self) -> list[UserResponse]:
        logger.info("Fetching users from repository")
        users = self.user_repository.get_users()
        logger.info("Fetched users from repository")
        # ドメインモデルからDTOへの変換
        return [UserResponse.model_validate(user.model_dump()) for user in users]
