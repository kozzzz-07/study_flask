from application.ports.user_dto import UserResponse, UserCreateDTO
from application.ports.user_repository_port import IUserRepository
from utils.logging import get_logger
from utils.decorators import log_errors
from application.exceptions import UserNotFoundError
from domain.user_domain import User


logger = get_logger(__name__)


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    @log_errors(logger_name=__name__)
    def get_users(self) -> list[UserResponse]:
        logger.info("Fetching users from repository")
        users = self.user_repository.get_users()
        if (
            not users
        ):  # 例として、ビジネスロジック層でユーザーが見つからない場合に例外を発生させる
            raise UserNotFoundError("No users found in the system.")
        logger.info("Fetched users from repository")
        # ドメインモデルからDTOへの変換
        return [UserResponse.model_validate(user.model_dump()) for user in users]

    @log_errors(logger_name=__name__)
    def add_user(self, user_create_dto: UserCreateDTO) -> UserResponse:
        logger.info(f"Adding user: {user_create_dto.name}")
        user = User(name=user_create_dto.name, age=user_create_dto.age, nickname=user_create_dto.nickname)
        created_user = self.user_repository.add_user(user)
        logger.info(f"User added with ID: {created_user.id}")
        return UserResponse.model_validate(created_user.model_dump())
