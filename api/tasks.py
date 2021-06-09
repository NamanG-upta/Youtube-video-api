from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .utils import fetch_videos_from_youtube_and_store_in_db


@shared_task
def fetch_videos():
    fetch_videos_from_youtube_and_store_in_db()
