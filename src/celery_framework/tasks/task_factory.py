"""Factory for creating Celery tasks."""
import logging
from typing import Callable
from celery import Celery
from .task import Task

logger = logging.getLogger(__name__)


class TaskFactory:
    """Factory for creating tasks from functions."""

    def __init__(self, celery_app: Celery):
        """
        Initialize task factory.

        Args:
            celery_app: Celery application instance
        """
        self.celery_app = celery_app

    def create(self, func: Callable, name: str = None, **options) -> Task:
        """
        Create a Celery task from a function.

        Args:
            func: The function to wrap as a task
            name: Task name (optional)
            **options: Celery task options

        Returns:
            Task wrapper instance
        """
        task_name = name or f"{func.__module__}.{func.__name__}"

        # Create Celery task
        celery_task = self.celery_app.task(
            name=task_name,
            **options
        )(func)

        logger.debug(f"Created task: {task_name}")

        return Task(celery_task, func, task_name)

    def __call__(self, func: Callable, name: str = None, **options) -> Task:
        """Alias for create method."""
        return self.create(func, name, **options)
