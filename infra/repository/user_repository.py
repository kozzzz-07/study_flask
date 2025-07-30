from application.ports.user_repository_port import IUserRepository
from domain.user_domain import User


class UserRepository(IUserRepository):
    def __init__(self, db):
        self.db = db

    def get_users(self, limit=100) -> list[User]:
        cursor = self.db.execute(
            "SELECT id, name, age, nickname FROM user LIMIT ?", (limit,)
        )
        users = cursor.fetchall()

        return [User(**dict(row)) for row in users]
