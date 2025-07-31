from flask import Blueprint, jsonify

from dependencies import get_user_service
from utils.logging import get_logger

user_bp = Blueprint("user", __name__)

logger = get_logger(__name__)


@user_bp.route("/users", methods=["GET"])
def get_users():
    logger.info("Fetching users")
    user_service = get_user_service()
    users_dto = user_service.get_users()  # DTOを受け取る
    logger.info(f"Fetched {len(users_dto)} users")
    # DTOを辞書に変換してからJSONにする
    return jsonify([user.model_dump() for user in users_dto])
