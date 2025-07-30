import sys
import os

from infra.client.db_client import get_db

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from infra.repository.user_repository import UserRepository


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
