"""Celery application wrapper."""
from celery import Celery
from omegaconf import DictConfig, OmegaConf

class CeleryApp:
    """Simple Celery application wrapper."""
    
    def __init__(self, config: DictConfig):
        """Initialize Celery app with config."""
        self.config = config
        self.app = self._create_app()
    
    def _create_app(self) -> Celery:
        """Create Celery app."""
        app_name = self.config.app.name if hasattr(self.config, 'app') else 'celery'
        app = Celery(app_name)
        
        # Apply celery config
        celery_config = OmegaConf.to_container(self.config.celery, resolve=True)
        
        # Add worker config
        if hasattr(self.config, 'worker'):
            worker_config = OmegaConf.to_container(self.config.worker, resolve=True)
            celery_config.update({f"worker_{k}": v for k, v in worker_config.items()})
        
        # Add task config
        if hasattr(self.config, 'task'):
            task_config = OmegaConf.to_container(self.config.task, resolve=True)
            celery_config.update({f"task_{k}": v for k, v in task_config.items()})
        
        app.conf.update(celery_config)
        return app


def create_app(config: DictConfig) -> CeleryApp:
    """Create Celery application."""
    return CeleryApp(config)
