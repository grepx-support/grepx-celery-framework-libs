import importlib
import inspect
import logging
from pathlib import Path
from typing import Callable

from celery_framework.src.tasks.task import Task
from celery_framework.src.tasks.task_factory import TaskFactory

logger = logging.getLogger(__name__)


class TaskRegistry:
    """Registry for managing tasks with auto-discovery."""

    def __init__(self, task_factory: TaskFactory):
        self._factory = task_factory
        self._tasks: dict[str, Task] = {}

    def register(self, name: str, func: Callable, **options) -> Task:
        """Register a single task."""
        task = self._factory(func, name=name, **options)
        self._tasks[name] = task
        logger.info(f"Registered task: {name}")
        return task

    def autodiscover(self, modules: list[str]):
        """Auto-discover and register tasks from modules."""
        for module_path in modules:
            try:
                module = importlib.import_module(module_path)
                self._discover_from_module(module)
            except Exception as e:
                logger.error(f"Failed to discover tasks from {module_path}: {e}")

    def autodiscover_from_path(self, base_path: str, pattern: str = "tasks.py"):
        """Auto-discover tasks from filesystem path."""
        path = Path(base_path)

        for task_file in path.rglob(pattern):
            module_path = self._path_to_module(task_file, path)
            try:
                module = importlib.import_module(module_path)
                self._discover_from_module(module)
            except Exception as e:
                logger.error(f"Failed to load {module_path}: {e}")

    def _discover_from_module(self, module):
        """Discover tasks from a module."""
        for name, obj in inspect.getmembers(module):
            if self._is_task_function(obj):
                task_name = getattr(obj, "__task_name__", f"{module.__name__}.{name}")
                task_options = getattr(obj, "__task_options__", {})
                self.register(task_name, obj, **task_options)

    def _is_task_function(self, obj) -> bool:
        """Check if object is a task function."""
        return (
                callable(obj) and
                hasattr(obj, "__task_name__") or
                (inspect.isfunction(obj) and not obj.__name__.startswith("_"))
        )

    def _path_to_module(self, file_path: Path, base_path: Path) -> str:
        """Convert file path to module path."""
        relative = file_path.relative_to(base_path)
        module_path = str(relative.with_suffix("")).replace("/", ".")
        return module_path

    def get(self, name: str) -> Task | None:
        """Get task by name."""
        return self._tasks.get(name)

    def all(self) -> dict[str, Task]:
        """Get all tasks."""
        return self._tasks.copy()

    def list_names(self) -> list[str]:
        """List all registered task names."""
        return list(self._tasks.keys())
