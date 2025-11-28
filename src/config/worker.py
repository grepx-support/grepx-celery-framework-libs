# src/celery_framework/config/worker.py
"""Worker configuration."""

from dataclasses import dataclass
from typing import Any

from .protocol import ConfigLoader


@dataclass
class WorkerConfig:
    """Worker process configuration."""

    prefetch_multiplier: int = 1
    max_tasks_per_child: int = 50

    @classmethod
    def from_dict(cls, config: dict[str, Any]) -> "WorkerConfig":
        """Create config from dictionary."""
        valid_keys = {k: v for k, v in config.items() if k in cls.__annotations__}
        return cls(**valid_keys)

    @classmethod
    def from_loader(cls, loader: ConfigLoader) -> "WorkerConfig":
        """Create config from ConfigLoader."""
        worker_config = loader.get("worker", {})
        if not worker_config:
            return cls()
        if isinstance(worker_config, dict):
            return cls.from_dict(worker_config)
        return cls.from_dict(worker_config.__dict__ if hasattr(worker_config, '__dict__') else {})

    def to_dict(self) -> dict:
        """Convert to Celery configuration format."""
        return {
            "worker_prefetch_multiplier": self.prefetch_multiplier,
            "worker_max_tasks_per_child": self.max_tasks_per_child,
        }
