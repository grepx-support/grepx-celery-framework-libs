# src/celery_framework/config/protocol.py
"""Configuration loader protocol."""

from typing import Protocol, Any


class ConfigLoader(Protocol):
    """Protocol for configuration loaders."""

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        ...

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        ...
