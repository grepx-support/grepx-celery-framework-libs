"""Celery Framework - Simple Celery wrapper."""

from .celery_app import CeleryApp, create_app

__version__ = "1.0.0"

__all__ = [
    "CeleryApp",
    "create_app",
]
