from flask import g
from infra.client.db_client import get_db
from infra.repository.user_repository import UserRepository
from services.user_service import UserService


def get_user_service():
    if "user_service" not in g:
        db = get_db()
        user_repository = UserRepository(db)
        g.user_service = UserService(user_repository)
    return g.user_service
