import os
from flask import Flask, request, jsonify, send_from_directory
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

app = Flask(__name__, static_folder="static")

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


# 例えば、Reactなどをbuildしたファイルをstatic配下に配置した場合、flaskから配信できる
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


@app.route("/error")
def trigger_error():
    1 / 0  # ZeroDivisionErrorを意図的に発生させる


# エラーハンドラーを登録
register_error_handlers(app)


app.register_blueprint(hello_bp)
app.register_blueprint(user_bp)
app.register_blueprint(db_bp)
