import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'action_weekly': {
        'task': 'app.celery.tasks.task_weekly_send',
        'schedule': crontab(hour=16, minute=22, day_of_week='thursday'),
    },
}

app.autodiscover_tasks()


