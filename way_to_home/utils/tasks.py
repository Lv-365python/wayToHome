"""This module provides celery tasks."""

from celery.schedules import crontab
from celery.task import periodic_task

from django.conf import settings
from notification.models import Notification
from .file_handlers import load_file, unzip_file


DEFAULT_RETRY_DELAY = 60
CLEANER_CTONTAB = crontab(hour=1, minute=30)
EASYWAY_CTONTAB = crontab(hour=2, day_of_week=1)


@periodic_task(bind=True,
               name='delete expired notifications',
               run_every=CLEANER_CTONTAB,
               ignore_result=True,
               default_retry_delay=DEFAULT_RETRY_DELAY)
def delete_expired_notifications(self):
    """Delete notifications that have expired datetime every day at 1:30 a.m."""
    retry = False

    notifications = Notification.get_expired()
    for notification_id in notifications.values_list('id', flat=True):
        if not Notification.delete_by_id(obj_id=notification_id):
            retry = True

    if retry:
        raise self.retry()


@periodic_task(bind=True,
               name='prepare static easy way data',
               ignore_results=True,
               run_every=EASYWAY_CTONTAB,
               default_retry_delay=DEFAULT_RETRY_DELAY)
def prepare_static_easy_way_data(self):
    """Provide preparing static data from EasyWay every Monday at 2 a.m."""
    url = 'http://track.ua-gis.com/gtfs/lviv/static/zip'

    loaded_file = load_file(url, save_to=settings.EASY_WAY_DIR)
    if not loaded_file:
        raise self.retry()

    is_unzipped = unzip_file(loaded_file, unzip_to=settings.EASY_WAY_DIR)
    if not is_unzipped:
        raise self.retry()
