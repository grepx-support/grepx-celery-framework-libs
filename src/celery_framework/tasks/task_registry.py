"""Registry for managing and discovering tasks."""
import importlib
import inspect
import logging
import sys
from pathlib import Path
from typing import Callable, Optional, Dict
from .task import Task
from .task_factory import TaskFactory

logger = logging.getLogger(__name__)


class TaskRegistry:
    """Registry for managing tasks with auto-discovery."""

    def __init__(self, task_factory: TaskFactory):
        """
        Initialize task registry.

        Args:
            task_factory: Factory for creating tasks
        """
        self._factory = task_factory
        self._tasks: Dict[str, Task] = {}

    def register(self, name: str, func: Callable, **options) -> Task:
        """
        Register a single task.

        Args:
            name: Task name
            func: Function to register as task
            **options: Celery task options

        Returns:
            Registered Task instance
        """
        if name in self._tasks:
            logger.warning(f"Task {name} already registered, overwriting")

        task = self._factory.create(func, name=name, **options)
        self._tasks[name] = task
        logger.info(f"✓ Registered task: {name}")
        return task

    def autodiscover(self, modules: list[str]) -> None:
        """
        Auto-discover and register tasks from modules.

        Args:
            modules: List of module paths (e.g., ['myapp.tasks', 'external.tasks'])
        """
        logger.info(f"Auto-discovering tasks from {len(modules)} module(s)")

        for module_path in modules:
            try:
                module = importlib.import_module(module_path)
                count = self._discover_from_module(module)
                logger.info(f"✓ Discovered {count} task(s) from {module_path}")
            except ImportError as e:
                logger.error(f"✗ Failed to import {module_path}: {e}")
            except Exception as e:
                logger.error(f"✗ Failed to discover tasks from {module_path}: {e}")

    def autodiscover_from_path(self, base_path: str, pattern: str = "tasks.py") -> None:
        """
        Auto-discover tasks from filesystem path.

        Args:
            base_path: Base directory path
            pattern: File pattern to match (e.g., 'tasks.py', '*_task.py')
        """
        path = Path(base_path).resolve()

        if not path.exists():
            logger.warning(f"✗ Path does not exist: {base_path}")
            return

        logger.info(f"Auto-discovering tasks from {base_path} (pattern: {pattern})")

        # Add base path to sys.path if not already there
        base_path_str = str(path.parent)
        if base_path_str not in sys.path:
            sys.path.insert(0, base_path_str)

        task_files = list(path.rglob(pattern))
        logger.info(f"Found {len(task_files)} file(s) matching pattern '{pattern}'")

        for task_file in task_files:
            module_path = self._path_to_module(task_file, path)
            try:
                module = importlib.import_module(module_path)
                count = self._discover_from_module(module)
                logger.info(f"✓ Discovered {count} task(s) from {task_file}")
            except Exception as e:
                logger.error(f"✗ Failed to load {module_path}: {e}")

    def _discover_from_module(self, module) -> int:
        """
        Discover tasks from a module.

        Args:
            module: Python module to inspect

        Returns:
            Number of tasks discovered
        """
        count = 0
        for name, obj in inspect.getmembers(module):
            if self._is_task_function(obj):
                task_name = getattr(obj, "__task_name__", f"{module.__name__}.{name}")
                task_options = getattr(obj, "__task_options__", {})

                # Get the original function if wrapped
                func = getattr(obj, "__wrapped__", obj)
                self.register(task_name, func, **task_options)
                count += 1

        return count

    def _is_task_function(self, obj) -> bool:
        """
        Check if object is a task function.

        Args:
            obj: Object to check

        Returns:
            True if object is a task function
        """
        # Check if marked with @task decorator
        if hasattr(obj, "__is_task__") and obj.__is_task__:
            return True

        # Check if it's a callable with task metadata
        if callable(obj) and hasattr(obj, "__task_name__"):
            return True

        return False

    def _path_to_module(self, file_path: Path, base_path: Path) -> str:
        """
        Convert file path to module path.

        Args:
            file_path: Full path to file
            base_path: Base path to calculate relative module path

        Returns:
            Module path string
        """
        try:
            relative = file_path.relative_to(base_path)
        except ValueError:
            # If not relative to base_path, use absolute
            relative = file_path

        module_path = str(relative.with_suffix("")).replace("/", ".").replace("\\", ".")

        # Remove __init__ if present
        if module_path.endswith(".__init__"):
            module_path = module_path[:-9]

        return module_path

    def get(self, name: str) -> Optional[Task]:
        """
        Get task by name.

        Args:
            name: Task name

        Returns:
            Task instance or None
        """
        return self._tasks.get(name)

    def all(self) -> Dict[str, Task]:
        """Get all registered tasks."""
        return self._tasks.copy()

    def list_names(self) -> list[str]:
        """List all registered task names."""
        return sorted(self._tasks.keys())

    def __len__(self) -> int:
        """Get number of registered tasks."""
        return len(self._tasks)

    def __repr__(self) -> str:
        return f"<TaskRegistry: {len(self)} task(s)>"
