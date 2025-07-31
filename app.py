from flask import Flask, request
from dotenv import load_dotenv
import uuid

from route.hello import hello_bp
from route.user import user_bp
from infra.client.db_client import db_bp
from utils.logging import setup_logging, get_logger
from structlog.contextvars import bind_contextvars, clear_contextvars

load_dotenv()

# ロギング設定を初期化
setup_logging()
logger = get_logger(__name__)

app = Flask(__name__)

logger.info("Flask application started.")


@app.before_request
def before_request():
    """
    リクエストの開始時にコンテキスト情報をバインドする
    """
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    bind_contextvars(
        request_id=request_id,
        remote_addr=request.remote_addr,
        method=request.method,
        path=request.path,
    )


@app.after_request
def after_request(response):
    """
    リクエストの終了時にコンテキストをクリアする
    """
    clear_contextvars()
    return response


@app.route("/")
def hello_world():
    logger.info("Hello World endpoint was called.")
    return "<p>Hello, World!</p>"


@app.route("/error")
def trigger_error():
    try:
        1 / 0  # ZeroDivisionErrorを意図的に発生させる
    except ZeroDivisionError:
        logger.error("ZeroDivisionErrorが発生しました。", exc_info=True)
        return "<p>Error triggered and logged!</p>", 500


app.register_blueprint(hello_bp)
app.register_blueprint(user_bp)
app.register_blueprint(db_bp)
