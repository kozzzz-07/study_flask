import sys
import os

from infra.client.db_client import get_db

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from infra.repository.user_repository import UserRepository
from domain.user_domain import User


def test_get_users():
    with app.app_context():
        db = get_db()
        user_repository = UserRepository(db)
        users = user_repository.get_users()
        assert len(users) > 0


def test_get_users_with_limit():
    with app.app_context():
        db = get_db()
        user_repository = UserRepository(db)
        users = user_repository.get_users(limit=1)
        assert len(users) == 1


def test_add_user():
    with app.app_context():
        db = get_db()
        user_repository = UserRepository(db)
        initial_user_count = len(user_repository.get_users())

        new_user = User(name="Test User", age=25, nickname="Tester")
        created_user = user_repository.add_user(new_user)

        assert created_user.id is not None
        assert created_user.name == "Test User"
        assert created_user.age == 25
        assert created_user.nickname == "Tester"

        # ユーザーが追加されたことを確認
        users_after_add = user_repository.get_users()
        assert len(users_after_add) == initial_user_count + 1

        # 追加したユーザーが取得できることを確認
        found = False
        for user in users_after_add:
            if user.id == created_user.id:
                found = True
                break
        assert found

        # テスト後にデータをクリーンアップ（オプションだが推奨）
        db.execute("DELETE FROM user WHERE id = ?", (created_user.id,))
        db.commit()
