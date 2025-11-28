# src/celery_framework/config/loader.py
"""Hydra configuration loader."""

from typing import Any
from omegaconf import DictConfig, OmegaConf


class HydraConfigLoader:
    """Adapter for Hydra/OmegaConf configuration."""

    def __init__(self, config: DictConfig):
        self._config = config

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        try:
            return OmegaConf.select(self._config, key, default=default)
        except Exception:
            return default

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return OmegaConf.to_container(self._config, resolve=True)
