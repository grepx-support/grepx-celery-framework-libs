"""Task loader for loading tasks from configuration."""
import logging

from omegaconf import DictConfig

from .task_registry import TaskRegistry

logger = logging.getLogger(__name__)


class TaskLoader:
    """Load tasks using multiple strategies from configuration."""

    def __init__(self, registry: TaskRegistry):
        """
        Initialize task loader.

        Args:
            registry: Task registry instance
        """
        self.registry = registry

    def load_from_config(self, cfg: DictConfig) -> None:
        """
        Load tasks from Hydra configuration.

        Args:
            cfg: Tasks configuration (from cfg.tasks)
        """
        if not cfg:
            logger.info("No task configuration provided")
            return

        logger.info("=" * 60)
        logger.info("Loading tasks from configuration")
        logger.info("=" * 60)

        # Load from modules
        if 'modules' in cfg and cfg.modules:
            logger.info(f"Loading tasks from {len(cfg.modules)} module(s)")
            self.registry.autodiscover(list(cfg.modules))

        # Load from directories
        if 'directories' in cfg and cfg.directories:
            logger.info(f"Loading tasks from {len(cfg.directories)} director(ies)")
            for dir_cfg in cfg.directories:
                path = dir_cfg.path if hasattr(dir_cfg, 'path') else dir_cfg.get('path')
                pattern = (dir_cfg.pattern if hasattr(dir_cfg, 'pattern')
                           else dir_cfg.get('pattern', 'tasks.py'))
                self.registry.autodiscover_from_path(path, pattern)

        logger.info("=" * 60)
        logger.info(f"Total tasks registered: {len(self.registry)}")
        logger.info(f"Registered tasks: {', '.join(self.registry.list_names())}")
        logger.info("=" * 60)