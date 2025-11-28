# main.py
"""Application entry point with Hydra."""

import hydra
from omegaconf import DictConfig


@hydra.main(version_base=None, config_path="config", config_name="config")
def main(cfg: DictConfig):
    """Main application entry point."""

    loader = HydraConfigLoader(cfg)
    app_name = loader.get("app.name", "celery_app")

    app, registry = CeleryFactory.create_app(app_name, loader)

    # Your application logic here
    print(f"Environment: {cfg.app.environment}")
    print(f"Celery Broker: {cfg.celery.broker_url}")
    print(f"Worker Config: {cfg.worker}")

    return app, registry


if __name__ == "__main__":
    main()
