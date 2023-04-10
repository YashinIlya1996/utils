from functools import wraps
from time import sleep
from typing import Callable


def retry(count=5, exceptions=(Exception,), delay=0, retry_backoff=1,
          retry_callback: Callable[[int, Exception], bool] = None):
    """
    :param count: the number of repetitions when the exceptions listed in the argument `exceptions` occur
    :param exceptions: tuple of exceptions that will cause the decorated function to be called again
    :param delay: number of seconds between repeated function calls
    :param retry_backoff: multiplier, how many times the delay time between repeated calls increases
    :param retry_callback: a callback to which, in case of an exception, the number of the attempt and
     the object of the exception are transmitted. If the callback returns True, repeat attempts will stop
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_count = 0
            current_delay = delay
            while current_count < count:
                try:
                    result = func(*args, **kwargs)
                    return result
                except exceptions as e:
                    current_count += 1
                    if retry_callback is not None:
                        callback_result = retry_callback(current_count, e)
                        if callback_result:
                            break
                    if current_count == count:
                        raise e
                    sleep(current_delay)
                    current_delay *= retry_backoff

        return wrapper

    return decorator
