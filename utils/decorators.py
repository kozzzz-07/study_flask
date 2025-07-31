import functools
from utils.logging import get_logger

def log_errors(logger_name: str = "application"):
    """
    関数実行中に発生した例外をログに記録するデコレーター。
    """
    def decorator(func):
        logger = get_logger(logger_name)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # メソッドの場合、最初の引数 (self) をログから除外
                # argsが空でないことを確認し、最初の要素をスキップ
                cleaned_args = args[1:] if args else args

                logger.error(
                    "An error occurred during function execution.",
                    function=func.__name__,
                    args=cleaned_args,
                    kwargs=kwargs,
                    exc_info=True
                )
                raise # 例外を再送出
        return wrapper
    return decorator
