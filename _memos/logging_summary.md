## 構造化ロギング設定

### 概要

`structlog`ライブラリを利用して、アプリケーションのロギングを構造化ログ（JSON形式）で出力するように設定しました。
これにより、ログの追跡、検索、分析が容易になり、DatadogやElasticsearchなどの外部ツールとの連携もスムーズになります。

設定は `utils/logging.py` に集約されており、`app.py` で有効化されています。

### 主要な機能

#### 1. リクエストコンテキストの自動付与

Flaskの `before_request` フックを利用して、各リクエストのコンテキスト情報が、そのリクエスト内で発生する全てのログに自動的に付与されます。

**自動で付与される主な情報:**
*   `request_id`: 各リクエストに付与される一意なID
*   `remote_addr`: リクエスト元のIPアドレス
*   `method`: HTTPメソッド (e.g., `GET`, `POST`)
*   `path`: リクエストされたパス (e.g., `/users/123`)

この仕組みは `app.py` に実装されています。

```python
# app.py抜粋
@app.before_request
def before_request():
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    bind_contextvars(
        request_id=request_id,
        # ...その他の情報
    )

@app.after_request
def after_request(response):
    clear_contextvars()
    return response
```

#### 2. ロガーの取得と利用

各モジュールでログを出力するには、`utils.logging` から `get_logger` をインポートしてロガーを取得します。

**利用方法:**

```python
from utils.logging import get_logger

logger = get_logger(__name__)

def some_business_logic(user_id: int):
    # logger.info() を呼び出すだけで、上記のリクエスト情報が自動的に記録される
    logger.info("処理を開始しました。", user_id=user_id, status="running")
    
    try:
        # 何らかの処理
        result = 1 / 0
    except Exception as e:
        logger.error("予期せぬエラーが発生しました。", exc_info=True)
        raise
```

### ログ出力例

上記コードが `/users/` へのPOSTリクエストで実行された場合、コンソールには以下のようなJSONログが出力されます。
リクエストコンテキスト(`request_id`, `method`, `path`など)が自動で含まれていることがわかります。

```json
{
  "level": "info",
  "event": "処理を開始しました。",
  "user_id": 123,
  "status": "running",
  "logger": "services.some_service",
  "timestamp": "2023-10-27T12:34:56.789012Z",
  "request_id": "f8b1f2c4-7e3a-4b8c-8b7a-9c8d7e6f5a4b",
  "remote_addr": "127.0.0.1",
  "method": "POST",
  "path": "/users/"
}
```