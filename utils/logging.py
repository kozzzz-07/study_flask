import logging
import os
import structlog
from colorama import init as colorama_init
import sys


def setup_logging():
    """
    structlogのロギング設定を構成します。
    環境変数IS_DEBUGが'true'の場合、色付きコンソール出力を行います。
    それ以外の場合はJSON形式で出力します。
    """

    # 標準のlogging設定
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    # 環境変数をチェック
    if os.environ.get("IS_DEBUG") == "true":
        colorama_init()  # coloramaを初期化
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        processors.append(structlog.processors.JSONRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
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
