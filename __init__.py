# src/celery_framework/__init__.py
"""Generic Celery framework for distributed task execution."""

__all__ = [
    "CeleryConfig",
    "WorkerConfig",
    "TaskConfig",
    "TaskRegistry",
    "task",
]

from main.celery_framework import CeleryConfig, WorkerConfig, TaskConfig
from main.celery_framework import task
from main.celery_framework import TaskRegistry
