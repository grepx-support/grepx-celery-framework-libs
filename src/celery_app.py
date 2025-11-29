"""Celery application module for CLI usage."""
import logging
import os
from pathlib import Path

from omegaconf import OmegaConf

from .app import create_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def _load_config():
    """Load configuration from YAML file."""
    # Get the project root directory (parent of src)
    project_root = Path(__file__).parent.parent
    config_path = project_root / "config" / "config.yaml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    cfg = OmegaConf.load(config_path)
    
    # Override with environment variables if present
    if "APP_ENV" in os.environ:
        cfg.app.environment = os.environ["APP_ENV"]
    if "CELERY_BROKER_URL" in os.environ:
        cfg.celery.broker_url = os.environ["CELERY_BROKER_URL"]
    if "CELERY_RESULT_BACKEND" in os.environ:
        cfg.celery.result_backend = os.environ["CELERY_RESULT_BACKEND"]
    
    return cfg


# Initialize Celery app at module level for CLI usage
try:
    cfg = _load_config()
    celery_app_wrapper = create_app(cfg)
    app = celery_app_wrapper.app  # Expose the Celery app instance
    logger.info("Celery app initialized successfully")
    logger.info(f"Registered tasks: {celery_app_wrapper.list_tasks()}")
except Exception as e:
    logger.error(f"Failed to initialize Celery app: {e}", exc_info=True)
    raise

