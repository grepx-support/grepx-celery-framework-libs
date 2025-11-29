"""Main entry point for Celery framework."""
import logging
import hydra
from omegaconf import DictConfig
from app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@hydra.main(config_path="../config", config_name="config", version_base=None)
def main(cfg: DictConfig) -> None:
    """
    Main entry point.

    Args:
        cfg: Hydra configuration
    """
    logger.info("Starting Celery Framework")
    # logger.info(f"Environment: {cfg.app.environment}")

    # Create Celery app
    celery_app = create_app(cfg)

    logger.info(f"Registered tasks: {celery_app.list_tasks()}")
    logger.info("Celery framework ready!")

    # Keep the app instance available
    return celery_app.app


if __name__ == "__main__":
    main()
