# src/celery_framework/config/celery.py
"""Celery broker and serialization configuration."""

from dataclasses import dataclass
from typing import Any

from .protocol import ConfigLoader


@dataclass
class CeleryConfig:
    """Celery broker and serialization configuration."""

    broker_url: str
    result_backend: str
    task_serializer: str = "json"
    result_serializer: str = "json"
    accept_content: list[str] = None
    timezone: str = "UTC"
    enable_utc: bool = True

    def __post_init__(self):
        if self.accept_content is None:
            self.accept_content = ["json"]

    @classmethod
    def from_dict(cls, config: dict[str, Any]) -> "CeleryConfig":
        """Create config from dictionary."""
        valid_keys = {k: v for k, v in config.items() if k in cls.__annotations__}
        return cls(**valid_keys)

    @classmethod
    def from_loader(cls, loader: ConfigLoader) -> "CeleryConfig":
        """Create config from ConfigLoader."""
        celery_config = loader.get("celery", {})
        if isinstance(celery_config, dict):
            return cls.from_dict(celery_config)
        return cls.from_dict(celery_config.__dict__ if hasattr(celery_config, '__dict__') else {})

    def to_dict(self) -> dict:
        """Convert to dictionary for Celery app configuration."""
        return {
            "broker_url": self.broker_url,
            "result_backend": self.result_backend,
            "task_serializer": self.task_serializer,
            "result_serializer": self.result_serializer,
            "accept_content": self.accept_content,
            "timezone": self.timezone,
            "enable_utc": self.enable_utc,
        }