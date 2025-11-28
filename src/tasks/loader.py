# src/celery_framework/loader.py
"""Task loader with multiple discovery strategies."""

import logging
from typing import List

from celery_framework.src.tasks.task_registry import TaskRegistry

logger = logging.getLogger(__name__)


class TaskLoader:
    """Load tasks using multiple strategies."""

    def __init__(self, registry: TaskRegistry):
        self.registry = registry

    def load_from_modules(self, module_paths: List[str]):
        """Load tasks from specific module paths."""
        logger.info(f"Loading tasks from modules: {module_paths}")
        self.registry.autodiscover(module_paths)

    def load_from_directory(self, directory: str, pattern: str = "tasks.py"):
        """Load tasks from directory."""
        logger.info(f"Loading tasks from directory: {directory}")
        self.registry.autodiscover_from_path(directory, pattern)

    def load_from_config(self, config_loader):
        """Load tasks from configuration."""
        task_modules = config_loader.get("task_modules", [])
        task_directories = config_loader.get("task_directories", [])

        if task_modules:
            self.load_from_modules(task_modules)

        for directory_config in task_directories:
            if isinstance(directory_config, dict):
                path = directory_config.get("path")
                pattern = directory_config.get("pattern", "tasks.py")
                self.load_from_directory(path, pattern)
            else:
                self.load_from_directory(directory_config)
