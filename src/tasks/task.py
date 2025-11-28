import logging
from typing import Protocol, Any

logger = logging.getLogger(__name__)


class Task(Protocol):
    """Task protocol."""

    name: str

    def delay(self, *args, **kwargs) -> Any:
        """Execute task asynchronously."""
        ...

    def apply_async(self, *args, **kwargs) -> Any:
        """Execute task with options."""
