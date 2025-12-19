"""Example Celery app for testing celery_framework."""

from pathlib import Path
from omegaconf import OmegaConf
from src.main.celery_framework import create_app

# Load config from config directory
config_path = Path(__file__).parent / "src/main/resources" / "config.yaml"
config = OmegaConf.load(config_path)

# Create Celery app
celery_wrapper = create_app(config)
app = celery_wrapper.app


# Example task
@app.task
def hello():
    return "Hello from celery_framework!"
