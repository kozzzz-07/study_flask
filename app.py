from flask import Flask, request, jsonify
from dotenv import load_dotenv
import uuid

from route.hello import hello_bp
from route.user import user_bp
from infra.client.db_client import db_bp
from utils.logging import setup_logging, get_logger
from structlog.contextvars import bind_contextvars, clear_contextvars
from application.error_handlers import register_error_handlers  # 追加

load_dotenv()

# ロギング設定を初期化
setup_logging()
logger = get_logger(__name__)

app = Flask(__name__)

logger.info("Flask application started.")


@app.before_request
def before_request():
    """
    リクエストの開始時にコンテキスト情報をバインドし、リクエストログを出力する
    """
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    bind_contextvars(
        request_id=request_id,
        remote_addr=request.remote_addr,
        method=request.method,
        path=request.path,
    )
    logger.info(
        "Incoming request",
        request_id=request_id,
        remote_addr=request.remote_addr,
        method=request.method,
        path=request.path,
    )


@app.after_request
def after_request(response):
    """
    リクエストの終了時にレスポンスログを出力し、コンテキストをクリアする
    """
    logger.info(
        "Outgoing response",
        status_code=response.status_code,
        content_length=response.content_length,
    )
    clear_contextvars()
    return response


@app.route("/")
def hello_world():
    logger.info("Hello World endpoint was called.")
    return "<p>Hello, World!</p>"


@app.route("/error")
def trigger_error():
    1 / 0  # ZeroDivisionErrorを意図的に発生させる


# エラーハンドラーを登録
register_error_handlers(app)


app.register_blueprint(hello_bp)
app.register_blueprint(user_bp)
app.register_blueprint(db_bp)
