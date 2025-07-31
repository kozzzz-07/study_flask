from application.ports.user_repository_port import IUserRepository
from domain.user_domain import User
from utils.logging import get_logger
from utils.decorators import log_errors


logger = get_logger(__name__)


# SQLiteに実装が依存しているが、利用する側はIUserRepositoryを見るだけで良い
class UserRepository(IUserRepository):
    def __init__(self, db):
        self.db = db

    @log_errors(logger_name=__name__)
    def get_users(self, limit=100) -> list[User]:
        logger.info(f"Fetching users with limit: {limit}")
        cursor = self.db.execute(
            "SELECT id, name, age, nickname FROM user LIMIT ?", (limit,)
        )
        users = cursor.fetchall()

        logger.info(f"Fetched users: {len(users)}")
        return [User(**dict(row)) for row in users]
