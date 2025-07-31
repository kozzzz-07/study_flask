from flask import Blueprint, jsonify, request

from dependencies import get_user_service
from utils.logging import get_logger
from application.ports.user_dto import UserCreateDTO

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


@user_bp.route("/users", methods=["POST"])
def add_user():
    logger.info("Adding new user")
    user_data = request.get_json()
    if not user_data:
        logger.warning("No user data provided in request")
        return jsonify({"error": "No user data provided"}), 400

    user_create_dto = UserCreateDTO(**user_data)
    user_service = get_user_service()
    created_user_dto = user_service.add_user(user_create_dto)
    logger.info(f"User added: {created_user_dto.id}")
    return jsonify(created_user_dto.model_dump()), 201
