"""This module provides tasks for notifications."""

from celery.schedules import crontab
from celery.task import periodic_task

from notification.models import Notification


@periodic_task(bind=True,
               name='delete expired notifications',
               run_every=(crontab(hour=1, minute=30)),
               ignore_result=True,
               default_retry_delay=60)
def delete_expired_notifications(self):
    """Delete notifications that have expired datetime every day at 1:30 a.m."""
    retry = False

    notifications = Notification.get_expired()
    for notification_id in notifications.values_list('id', flat=True):
        if not Notification.delete_by_id(obj_id=notification_id):
            retry = True

    if retry:
        raise self.retry()
