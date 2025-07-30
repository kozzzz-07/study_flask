from flask import Blueprint, request
from markupsafe import escape

from utils.logging import get_logger


logger = get_logger(__name__)

hello_bp = Blueprint("hello", __name__)


@hello_bp.route("/hello", methods=["GET"])
def hello():
    logger.info("Start: /hello")
    name = request.args.get("name")
    logger.info("End: /hello")
    return f"hello, {name}"


@hello_bp.route("/hello2/<name>", methods=["GET"])
def hello2(name):
    return f"hello, {escape(name)}"
