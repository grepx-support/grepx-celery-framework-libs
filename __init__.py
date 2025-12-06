# src/celery_framework/__init__.py
"""Generic Celery framework for distributed task execution."""

__all__ = [
    "CeleryConfig",
    "WorkerConfig",
    "TaskConfig",
    "TaskRegistry",
    "task",
]

from src.celery_framework.config import CeleryConfig, WorkerConfig, TaskConfig
from src.celery_framework.tasks.decorators import task
from src.celery_framework.tasks.task_registry import TaskRegistry
