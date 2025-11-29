"""Celery application factory."""
import logging

from celery import Celery
from omegaconf import DictConfig, OmegaConf

# Handle both relative imports (when used as package) and absolute imports (when run as script)
try:
    from .tasks import TaskFactory, TaskRegistry, TaskLoader
except ImportError:
    from tasks import TaskFactory, TaskRegistry, TaskLoader

logger = logging.getLogger(__name__)


class CeleryApp:
    """Celery application wrapper with task management."""

    def __init__(self, cfg: DictConfig):
        """
        Initialize Celery application.

        Args:
            cfg: Hydra configuration
        """
        self.cfg = cfg
        self.app = self._create_celery_app()
        self.registry = None
        self.loader = None

    def _create_celery_app(self) -> Celery:
        """Create and configure Celery application."""
        app_name = self.cfg.app.name
        logger.info(f"Creating Celery app: {app_name}")

        app = Celery(app_name)

        # Merge all sections into Celery config
        celery_config = OmegaConf.to_container(self.cfg.celery, resolve=True)

        # Add worker settings with proper prefixes
        if 'worker' in self.cfg:
            worker_cfg = OmegaConf.to_container(self.cfg.worker, resolve=True)
            celery_config.update({f"worker_{k}": v for k, v in worker_cfg.items()})

        # Add task settings with proper prefixes
        if 'task' in self.cfg:
            task_cfg = OmegaConf.to_container(self.cfg.task, resolve=True)
            celery_config.update({f"task_{k}": v for k, v in task_cfg.items()})

        app.conf.update(celery_config)

        logger.info(f"✓ Celery app configured")
        return app

    def load_tasks(self) -> None:
        """Load tasks from configuration."""
        # Create task management components
        factory = TaskFactory(self.app)
        self.registry = TaskRegistry(factory)
        self.loader = TaskLoader(self.registry)

        # Load tasks
        self.loader.load_from_config(self.cfg.get('tasks'))

    def get_task(self, name: str):
        """Get a registered task by name."""
        if not self.registry:
            raise RuntimeError("Tasks not loaded. Call load_tasks() first.")
        return self.registry.get(name)

    def list_tasks(self) -> list[str]:
        """List all registered task names."""
        if not self.registry:
            return []
        return self.registry.list_names()


def create_app(cfg: DictConfig) -> CeleryApp:
    """
    Factory function to create Celery application.

    Args:
        cfg: Hydra configuration

    Returns:
        CeleryApp instance
    """
    celery_app = CeleryApp(cfg)
    celery_app.load_tasks()
    return celery_app
