import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from services.user_service import UserService


def test_get_users():
    # TODO: このテストはUserRepositoryの具体的な実装に依存してしまっている。
    # 本来であれば、UserRepositoryをモック（偽のオブジェクト）に差し替えることで、
    # UserService単体のロジックをテストするべきである。
    # これにより、データベースの状態に依存しない、より高速で安定した単体テストになる。
    with app.app_context():
        user_service = UserService()
        users = user_service.get_users()
        assert isinstance(users, list)
        # DBにテストデータが実際に入っているので、件数も確認できる
        assert len(users) > 0
