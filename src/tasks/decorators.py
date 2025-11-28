# src/celery_framework/decorators.py
"""Task decorators for marking functions as tasks."""


def task(name: str = None, **options):
    """Decorator to mark a function as a Celery task."""

    def decorator(func):
        func.__task_name__ = name or f"{func.__module__}.{func.__name__}"
        func.__task_options__ = options
        return func

    return decorator
