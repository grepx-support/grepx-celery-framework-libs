# src/celery_framework/factory.py
"""Factory for creating Celery components."""
from . import CeleryConfig, WorkerConfig, TaskConfig, HydraConfigLoader
from .config_loader import ConfigLoader
from ..tasks.task_registry import TaskRegistry


class CeleryFactory:
    """Factory for creating Celery app and registry."""

    @staticmethod
    def create_app(
            name: str,
            config_loader: ConfigLoader,
    ) -> tuple[CeleryApp, TaskRegistry]:
        """Create Celery app and task registry from config loader."""

        celery_config = CeleryConfig.from_loader(config_loader)
        worker_config = WorkerConfig.from_loader(config_loader)
        task_config = TaskConfig.from_loader(config_loader)

        app = CeleryApp(name, celery_config, worker_config, task_config)
        registry = TaskRegistry(app.task)

        return app, registry

    @staticmethod
    def create_from_dict(
            name: str,
            config_dict: dict,
    ) -> tuple[CeleryApp, TaskRegistry]:
        """Create Celery app from dictionary config."""

        cfg = OmegaConf.create(config_dict)
        loader = HydraConfigLoader(cfg)

        return CeleryFactory.create_app(name, loader)
