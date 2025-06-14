"""
Celery application configuration for background tasks
"""

from celery import Celery

from core.config import get_settings

settings = get_settings()

# Create Celery app
celery_app = Celery(
    "strumind",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "tasks.analysis.tasks",
        "tasks.design.tasks",
        "tasks.export.tasks",
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Task routing
celery_app.conf.task_routes = {
    "tasks.analysis.*": {"queue": "analysis"},
    "tasks.design.*": {"queue": "design"},
    "tasks.export.*": {"queue": "export"},
}