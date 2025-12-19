# src/celery_framework/__init__.py
"""Generic Celery framework for distributed task execution."""

__all__ = [
    "create_app",
]
from main.celery_framework import create_app
