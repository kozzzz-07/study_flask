## ロギング設計思想と実装方針

### 1. 設計思想

本アプリケーションのロギングは、以下の設計思想に基づいています。

*   **構造化ロギング (Structured Logging):** `structlog` を利用し、ログをJSON形式で出力することで、機械可読性を高め、ログの集約・分析・検索を容易にします。これにより、DatadogやElasticsearchなどの外部ログ管理システムとの連携がスムーズになります。
*   **関心の分離 (Separation of Concerns):** ビジネスロジックとロギング処理を明確に分離し、各コンポーネントが本来の責務に集中できるようにします。
*   **トレーサビリティ (Traceability):** リクエストIDやモジュール名など、ログに豊富なコンテキスト情報を含めることで、問題発生時の原因特定や処理フローの追跡を容易にします。
*   **一貫性 (Consistency):** アプリケーション全体でロギングのフォーマット、レベル、エラーハンドリングの挙動を一貫させます。
*   **開発・運用効率の向上:** 開発環境での視認性（色付きログ）と、本番環境でのエラー監視・分析（構造化ログ、Sentry連携）の両方を考慮します。

### 2. ロギング基盤 (`utils/logging.py`, `utils/decorators.py`)

*   **`utils/logging.py`:**
    *   `setup_logging()`: `structlog` の初期設定を行い、ログの出力形式（開発環境では色付きコンソール、本番環境ではJSON）を環境変数 `IS_DEBUG` に応じて切り替えます。
    *   `get_logger(name: str)`: `structlog.get_logger(name)` をラップし、設定済みのロガーインスタンスを提供します。ロガー名には `__name__` を使用することを推奨し、ログの発生元モジュールを正確に特定できるようにします。
*   **`utils/decorators.py`:**
    *   `log_errors(logger_name: str = "application")`: 関数実行中に発生した予期せぬ例外を自動的にキャッチし、ログに記録するデコレーターです。
        *   `logger_name` で指定されたロガーを使用します。
        *   例外発生時の関数名、引数（`self` を除く）、キーワード引数、スタックトレース (`exc_info=True`) をログに含めます。
        *   ログ記録後に例外を再送出 (`raise`) し、上位層でのエラーハンドリングに委ねます。

### 3. 層別実装方針

#### 3.1. Web層 (`app.py`, ルートハンドラー)

Web層は、外部からのリクエストを受け付け、レスポンスを返す役割を担います。ロギングとエラーハンドリングの最終的な窓口となります。

*   **リクエスト/レスポンスロギング:**
    *   `@app.before_request`: 各リクエストの開始時に、`request_id` (X-Request-IDヘッダーまたはUUID)、`remote_addr`、`method`、`path` などのコンテキスト情報を `structlog.contextvars.bind_contextvars` でバインドし、`logger.info("Incoming request")` でログを出力します。これにより、そのリクエスト内で発生する全てのログにこれらの情報が自動的に付与されます。
    *   `@app.after_request`: 各リクエストの終了時に、`logger.info("Outgoing response")` でレスポンスのステータスコードやサイズなどをログに出力し、`structlog.contextvars.clear_contextvars` でコンテキスト変数をクリアします。
*   **グローバルエラーハンドリング:**
    *   `application/error_handlers.py` に定義された `register_error_handlers(app)` 関数を `app.py` で呼び出し、アプリケーション全体のエラーハンドリングを一元化します。
    *   **`@app.errorhandler(ApplicationError)`:** アプリケーション固有のカスタム例外（後述）をキャッチし、JSON形式のエラーレスポンスを返します。
    *   **`@app.errorhandler(HTTPException)`:** FlaskやWerkzeugが自動的に発生させるHTTPエラー（例: 404 Not Found, 405 Method Not Allowed）をキャッチし、JSON形式で返します。
    *   **`@app.errorhandler(Exception)`:** 上記でキャッチされなかった全ての予期せぬPython例外をキャッチする最終的な安全網です。500 Internal Server Errorとして処理し、詳細なエラーはログに記録しつつ、ユーザーには一般的なエラーメッセージを返します。
*   **ルートハンドラー:**
    *   ルートハンドラー自体は、主にビジネスロジック層のサービスを呼び出し、その結果をHTTPレスポンスに変換することに集中します。
    *   予期される入力バリデーションエラーなど、ルート固有のビジネスロジックエラーは、カスタム例外を `raise` することで、グローバルエラーハンドラーに処理を委ねます。

#### 3.2. ビジネスロジック層 (`services`, `domain`)

ビジネスロジック層は、アプリケーションの主要な機能とビジネスルールを実装します。

*   **ロガーの取得:** 各サービスやドメインモジュール内で `logger = get_logger(__name__)` を使用し、モジュール固有のロガーインスタンスを取得します。
*   **カスタム例外の利用:**
    *   `application/exceptions.py` に、`werkzeug.exceptions.HTTPException` を継承したカスタム例外クラス（例: `ApplicationError`, `UserNotFoundError`, `InvalidInputError`）を定義します。
    *   ビジネスルール違反や特定の条件（例: ユーザーが見つからない）が発生した場合に、これらのカスタム例外を `raise` します。これにより、エラーの種類が明確になり、Web層のグローバルエラーハンドラーで適切に処理されます。
*   **エラーロギングデコレーターの適用:**
    *   サービス層のメソッドには `@log_errors(logger_name=__name__)` デコレーターを適用します。これにより、メソッド内で発生した予期せぬ例外が自動的にログに記録され、スタックトレースや引数情報がログに含まれます。

#### 3.3. 下位層 (`infra/repository`, `infra/client`)

下位層は、データベースアクセスや外部API連携など、インフラストラクチャに関する処理を担います。

*   **ロガーの取得:** 各リポジトリやクライアントモジュール内で `logger = get_logger(__name__)` を使用し、モジュール固有のロガーインスタンスを取得します。
*   **エラーロギングデコレーターの適用:**
    *   データベース操作や外部サービス呼び出しを行うメソッドには、ビジネスロジック層と同様に `@log_errors(logger_name=__name__)` デコレーターを適用します。これにより、インフラ層で発生した技術的なエラー（例: データベース接続エラー、APIタイムアウト）が詳細にログに記録され、上位層に伝播されます。
*   **技術的例外の変換:**
    *   データベース固有の例外や外部APIのエラーなど、技術的な例外は、必要に応じてアプリケーション固有のカスタム例外（例: `DatabaseConnectionError` のような `ApplicationError` のサブクラス）に変換して `raise` することを検討します。これにより、上位層はインフラの詳細に依存せずにエラーを処理できます。

### ログ出力例

#### 正常リクエストのログ (Incoming/Outgoing)

```json
{"event": "Incoming request", "request_id": "...", "remote_addr": "127.0.0.1", "method": "GET", "path": "/users", "logger": "app", "level": "info", "timestamp": "..."}
{"event": "Fetching users from repository", "logger": "infra.repository.user_repository", "level": "info", "timestamp": "...", "request_id": "...", "remote_addr": "127.0.0.1", "method": "GET", "path": "/users"}
{"event": "Fetched users from repository", "logger": "services.user_service", "level": "info", "timestamp": "...", "request_id": "...", "remote_addr": "127.0.0.1", "method": "GET", "path": "/users"}
{"event": "Outgoing response", "status_code": 200, "content_length": 123, "logger": "app", "level": "info", "timestamp": "...", "request_id": "...", "remote_addr": "127.0.0.1", "method": "GET", "path": "/users"}
```

#### カスタム例外発生時のログ (`UserNotFoundError` の例)

```json
{"event": "Incoming request", "request_id": "...", "remote_addr": "127.0.0.1", "method": "GET", "path": "/users", "logger": "app", "level": "info", "timestamp": "..."}
{"event": "Fetching users from repository", "logger": "infra.repository.user_repository", "level": "info", "timestamp": "...", "request_id": "...", "remote_addr": "127.0.0.1", "method": "GET", "path": "/users"}
{"event": "An error occurred during function execution.", "function": "get_users", "args": [], "kwargs": {}, "logger": "services.user_service", "level": "error", "exception": "Traceback (most recent call last):
  File "/path/to/utils/decorators.py", line XX, in wrapper
    return func(*args, **kwargs)
  File "/path/to/services/user_service.py", line XX, in get_users
    raise UserNotFoundError("No users found in the system.")
application.exceptions.UserNotFoundError: 404 Not Found: No users found in the system.", "timestamp": "...", "request_id": "...", "remote_addr": "127.0.0.1", "method": "GET", "path": "/users"}
{"event": "Application error caught: User not found.", "logger": "app", "level": "warning", "exception": "Traceback (most recent call last):
  File "/path/to/flask/app.py", line XX, in full_dispatch_request
    rv = self.dispatch_request()
  File "/path/to/flask/app.py", line YY, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
  File "/path/to/route/user.py", line ZZ, in get_users
    users = user_service.get_users()
  File "/path/to/utils/decorators.py", line XX, in wrapper
    raise # 例外を再送出
  File "/path/to/services/user_service.py", line XX, in get_users
    raise UserNotFoundError("No users found in the system.")
application.exceptions.UserNotFoundError: 404 Not Found: No users found in the system.", "timestamp": "...", "request_id": "...", "remote_addr": "127.0.0.1", "method": "GET", "path": "/users"}
{"event": "Outgoing response", "status_code": 404, "content_length": 70, "logger": "app", "level": "info", "timestamp": "...", "request_id": "...", "remote_addr": "127.0.0.1", "method": "GET", "path": "/users"}
```

#### 予期せぬPython例外発生時のログ (`ZeroDivisionError` の例)

```json
{"event": "Incoming request", "request_id": "...", "remote_addr": "127.0.0.1", "method": "GET", "path": "/error", "logger": "app", "level": "info", "timestamp": "..."}
{"event": "Unhandled generic exception: division by zero", "logger": "app", "level": "error", "exception": "Traceback (most recent call last):
  File "/path/to/flask/app.py", line XX, in full_dispatch_request
    rv = self.dispatch_request()
  File "/path/to/flask/app.py", line YY, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**req.view_args)
  File "/path/to/app.py", line ZZ, in trigger_error
    1 / 0
ZeroDivisionError: division by zero", "timestamp": "...", "request_id": "...", "remote_addr": "127.0.0.1", "method": "GET", "path": "/error"}
{"event": "Outgoing response", "status_code": 500, "content_length": 60, "logger": "app", "level": "info", "timestamp": "...", "request_id": "...", "remote_addr": "127.0.0.1", "method": "GET", "path": "/error"}
```
