"""Task decorators for marking functions as tasks."""
from typing import Callable, Any
import functools


def task(name: str = None, **options) -> Callable:
    """
    Decorator to mark a function as a Celery task.

    Args:
        name: Optional task name. If not provided, uses module.function_name
        **options: Additional Celery task options (bind, max_retries, etc.)

    Example:
        @task(name="my_task", bind=True, max_retries=3)
        def my_function(self, x, y):
            return x + y
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper.__task_name__ = name or f"{func.__module__}.{func.__name__}"
        wrapper.__task_options__ = options
        wrapper.__is_task__ = True
        wrapper.__wrapped__ = func

        return wrapper

    return decorator
