from werkzeug.exceptions import HTTPException

class ApplicationError(HTTPException):
    """アプリケーションの基底例外クラス"""
    code = 500 # デフォルトのHTTPステータスコード
    description = "An unexpected error occurred."

    def __init__(self, description=None, code=None, payload=None):
        super().__init__(description or self.description)
        if code is not None:
            self.code = code
        self.payload = payload

    def to_dict(self):
        """JSONレスポンスのために辞書形式に変換"""
        rv = dict(self.payload or ())
        rv['message'] = self.description
        rv['code'] = self.code
        return rv

class UserNotFoundError(ApplicationError):
    code = 404
    description = "User not found."

class InvalidInputError(ApplicationError):
    code = 400
    description = "Invalid input provided."
