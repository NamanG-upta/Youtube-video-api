
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# from celery.schedule import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "youtube_fetch_api.settings")

app = Celery("youtube_fetch_api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "every-600-seconds": {
        "task": "api.tasks.fetch_videos",
        "schedule": 600.0,
        "args": (""),
    }
}

app.autodiscover_tasks()