import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app
from infra.repository.user_repository import UserRepository


def test_get_users():
    with app.app_context():
        user_repository = UserRepository()
        users = user_repository.get_users()
        assert len(users) > 0
