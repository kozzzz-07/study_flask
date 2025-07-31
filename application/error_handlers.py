from flask import jsonify
from werkzeug.exceptions import HTTPException
from application.exceptions import ApplicationError
from utils.logging import get_logger
from pydantic import ValidationError # PydanticのValidationErrorをインポート

logger = get_logger(__name__)

def register_error_handlers(app):
    """
    Flaskアプリケーションにグローバルエラーハンドラーを登録します。
    """

    # 1. カスタムApplicationErrorのハンドリング
    @app.errorhandler(ApplicationError)
    def handle_application_error(error):
        # ApplicationErrorは既に下位層でログされているはずなので、ここではログレベルをwarningにするなど調整可能
        logger.warning(f"Application error caught: {error.description}", exc_info=True)
        response = jsonify(error.to_dict())
        response.status_code = error.code
        return response

    # 2. PydanticのValidationErrorのハンドリング
    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        logger.warning(f"Pydantic validation error caught: {e.errors()}", exc_info=True)
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400

    # 3. WerkzeugのHTTPExceptionのハンドリング（404, 405, 500など）
    # これにより、Flaskが自動的に発生させるHTTPエラーもJSONで返せる
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        # ドキュメントの例を参考に、JSONレスポンスを生成
        logger.warning(f"HTTP exception caught: {e.code} - {e.description}", exc_info=True)
        response = jsonify({
            "message": e.description,
            "code": e.code,
            "name": e.name,
        })
        response.status_code = e.code
        return response

    # 4. その他の予期せぬPython例外のハンドリング（最終的な安全網）
    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        # ここに到達するエラーは、下位レイヤーでログ済みの場合が多いが、
        # 念のためログレベルをerrorで記録
        logger.error(f"Unhandled generic exception: {error}", exc_info=True)
        response = jsonify({
            "message": "An unexpected internal server error occurred.",
            "code": 500
        })
        response.status_code = 500
        return response
