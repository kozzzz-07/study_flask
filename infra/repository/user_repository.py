from domain.user_domain import User
from infra.client.db_client import get_db


class UserRepository:
    def get_users(self, limit=100) -> list[User]:
        db = get_db()
        cursor = db.execute(
            "SELECT id, name, age, nickname FROM user LIMIT ?", (limit,)
        )
        users = cursor.fetchall()

        return [User(**dict(row)) for row in users]
