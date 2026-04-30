from celery import Celery
from celery.schedules import crontab

from app.config import settings


celery_app = Celery(
    "gh_recruitment",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)
celery_app.conf.timezone = "UTC"
celery_app.conf.beat_schedule = {
    "gmail-import-every-5-min": {
        "task": "app.tasks.email_import_task.import_emails_task",
        "schedule": crontab(minute="*/5"),
    }
}
