# src/celery_framework/config/task.py
"""Task execution configuration."""

from dataclasses import dataclass
from typing import Any

from .protocol import ConfigLoader


@dataclass
class TaskConfig:
    """Task execution configuration."""

    track_started: bool = True
    time_limit: int = 1800
    soft_time_limit: int = 1500
    result_expires: int = 3600

    @classmethod
    def from_dict(cls, config: dict[str, Any]) -> "TaskConfig":
        """Create config from dictionary."""
        valid_keys = {k: v for k, v in config.items() if k in cls.__annotations__}
        return cls(**valid_keys)

    @classmethod
    def from_loader(cls, loader: ConfigLoader) -> "TaskConfig":
        """Create config from ConfigLoader."""
        task_config = loader.get("task", {})
        if not task_config:
            return cls()
        if isinstance(task_config, dict):
            return cls.from_dict(task_config)
        return cls.from_dict(task_config.__dict__ if hasattr(task_config, '__dict__') else {})

    def to_dict(self) -> dict:
        """Convert to Celery configuration format."""
        return {
            "task_track_started": self.track_started,
            "task_time_limit": self.time_limit,
            "task_soft_time_limit": self.soft_time_limit,
            "result_expires": self.result_expires,
        }
