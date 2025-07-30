from flask import Blueprint, jsonify
from services.user_service import UserService

user_bp = Blueprint("user", __name__)


@user_bp.route("/users", methods=["GET"])
def get_users():
    user_service = UserService()
    users = user_service.get_users()
    return jsonify(users)
