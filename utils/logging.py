import logging
import os
import structlog
from colorama import init as colorama_init


def setup_logging():
    """
    structlogのロギング設定を構成します。
    環境変数IS_DEBUGが'true'の場合、色付きコンソール出力を行います。
    それ以外の場合はJSON形式で出力します。
    """

    # 環境変数をチェック
    is_development = os.environ.get("IS_DEBUG") == "true"

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if is_development:
        colorama_init()  # coloramaを初期化
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        processors.append(structlog.processors.JSONRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str):
    """
    構成済みのロガーを取得します。

    Args:
        name (str): ロガーの名前。

    Returns:
        構成済みのロガーインスタンス。
    """
    return structlog.get_logger(name)
