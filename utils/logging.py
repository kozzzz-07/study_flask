import logging
import sys
import structlog

def setup_logging():
    """
    structlogのロギング設定を構成します。
    """
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
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