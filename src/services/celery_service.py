# src/services/celery_service.py
"""Celery service initialization with Hydra."""

from pathlib import Path
from hydra import compose, initialize_config_dir

from celery_framework.src.config import HydraConfigLoader
from celery_framework.src.config.factory import CeleryFactory


def create_celery_service(config_path: str = "config", env: str = "local"):
    """Create Celery service with auto task discovery."""

    config_dir = Path(config_path).absolute()

    with initialize_config_dir(config_dir=str(config_dir), version_base=None):
        overrides = [
            f"celery={env}",
            f"worker={env}",
        ]

        cfg = compose(config_name="config", overrides=overrides)
        loader = HydraConfigLoader(cfg)

        app_name = loader.get("app.name", "celery_app")
        app, registry, task_loader = CeleryFactory.create_app(
            app_name, loader, auto_discover=True
        )

        return app, registry, task_loader


celery_app, task_registry, task_loader = create_celery_service()
