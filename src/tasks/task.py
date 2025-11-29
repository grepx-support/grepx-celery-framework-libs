"""Task wrapper class."""
from typing import Callable, Any


class Task:
    """Wrapper around Celery task providing convenient interface."""

    def __init__(self, celery_task, func: Callable, name: str):
        """
        Initialize task wrapper.

        Args:
            celery_task: The Celery task object
            func: Original function
            name: Task name
        """
        self.celery_task = celery_task
        self.func = func
        self.name = name

    def __call__(self, *args, **kwargs) -> Any:
        """Execute task synchronously."""
        return self.func(*args, **kwargs)

    def delay(self, *args, **kwargs):
        """Execute task asynchronously using Celery."""
        return self.celery_task.delay(*args, **kwargs)

    def apply_async(self, args=None, kwargs=None, **options):
        """Execute task asynchronously with full options."""
        return self.celery_task.apply_async(args=args, kwargs=kwargs, **options)

    @property
    def task_id(self) -> str:
        """Get task name/id."""
        return self.name

    def __repr__(self) -> str:
        return f"<Task: {self.name}>"
