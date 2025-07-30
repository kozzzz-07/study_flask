from flask import Blueprint, request
from markupsafe import escape


hello_bp = Blueprint("hello", __name__)


@hello_bp.route("/hello", methods=["GET"])
def hello():
    name = request.args.get("name")
    return f"hello, {name}"


@hello_bp.route("/hello2/<name>", methods=["GET"])
def hello2(name):
    return f"hello, {escape(name)}"
