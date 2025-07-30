from infra.client.db_client import get_db


class UserRepository:
    def get_users(self, limit=100):
        db = get_db()
        cursor = db.execute(
            "SELECT id, name, age, nickname FROM user LIMIT ?", (limit,)
        )
        users = cursor.fetchall()

        return [dict(row) for row in users]
