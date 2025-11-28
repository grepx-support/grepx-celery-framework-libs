import logging
from typing import Protocol, Callable

logger = logging.getLogger(__name__)


class TaskFactory(Protocol):
    """Factory for creating tasks."""

    def __call__(self, func: Callable, **options) -> Task:
        """Create a task from function."""
        ...
