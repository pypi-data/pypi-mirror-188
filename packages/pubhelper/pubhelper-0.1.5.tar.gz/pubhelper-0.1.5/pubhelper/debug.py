import functools
import logging
import time


def timethis(fn=None, *, logger=None):
    """统计代码执行时间"""

    def inner(f):
        @functools.wraps(f)
        def _inner(*args, **kwargs):
            start = time.perf_counter()
            data = f(*args, **kwargs)
            end = time.perf_counter()
            logger.debug(f'func({f.__name__}): {(end - start) * 1000} ms')
            return data

        return _inner

    if not logger:
        logger = logging.getLogger('__time_count__')
    logger.setLevel(logging.DEBUG)
    return callable(fn) and inner(fn) or inner


def with_log(fn=None, *, logger=None):
    """打印日志"""

    def inner(f):
        @functools.wraps(f)
        def _inner(*args, **kwargs):
            logger.debug(
                f'func({f.__name__}) running(args={args}, kwargs={kwargs})')
            try:
                result = f(*args, **kwargs)
                logger.debug(f'func({f.__name__}) result: {result}')
            except Exception as e:
                return logger.error(f'func({f.__name__}) error: {e}')
            return result

        return _inner

    if not logger:
        logger = logging.getLogger('__with_log__')
    logger.setLevel(logging.DEBUG)
    return callable(fn) and inner(fn) or inner


__all__ = ('with_log', 'timethis')
