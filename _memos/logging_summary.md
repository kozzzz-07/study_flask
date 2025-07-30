## 構造化ロギング設定

### 概要

`structlog`ライブラリを利用して、アプリケーションのロギングを構造化ログ（JSON形式）で出力するように設定しました。
これにより、ログの追跡、検索、分析が容易になり、DatadogやElasticsearchなどの外部ツールとの連携もスムーズになります。

設定はすべて `utils/logging.py` に集約されています。

### 主要な関数

#### `setup_logging()`

アプリケーション全体のロギング設定を初期化する関数です。
アプリケーションの起動時に一度だけ呼び出す必要があります。

**呼び出し箇所:**
`app.py` の冒頭

```python
from utils.logging import setup_logging

# ロギング設定を初期化
setup_logging()
```

#### `get_logger(name: str)`

設定済みのロガーインスタンスを取得するための関数です。
各モジュールでログを出力したい場合、この関数を使用してください。

引数には、そのファイルの名前を示す `__name__` を渡すのが一般的です。

### 利用方法

各ファイルでロガーをインポートし、ログを出力します。

```python
from utils.logging import get_logger

logger = get_logger(__name__)

def some_business_logic(user_id: int):
    # `info`レベルのログ。追加情報をキーワード引数で渡せる
    logger.info("処理を開始しました。", user_id=user_id, status="running")
    
    try:
        # 何らかの処理
        result = 1 / 0
    except Exception as e:
        # `error`レベルのログ。`exc_info=True`で例外情報が付与される
        logger.error("予期せぬエラーが発生しました。", exc_info=True)
        raise
```

### ログ出力例

上記コードを実行すると、コンソールには以下のようなJSON形式のログが出力されます。

```json
{"level": "info", "event": "処理を開始しました。", "user_id": 123, "status": "running", "logger": "services.some_service", "timestamp": "2023-10-27T12:34:56.789012Z"}
{"level": "error", "event": "予期せぬエラーが発生しました。", "exc_info": "...", "logger": "services.some_service", "timestamp": "2023-10-27T12:34:56.790123Z"}
```
