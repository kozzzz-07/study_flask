from flask import Blueprint, jsonify

from dependencies import get_user_service

user_bp = Blueprint("user", __name__)


@user_bp.route("/users", methods=["GET"])
def get_users():
    user_service = get_user_service()
    users_dto = user_service.get_users()  # DTOを受け取る
    # DTOを辞書に変換してからJSONにする
    return jsonify([user.model_dump() for user in users_dto])
