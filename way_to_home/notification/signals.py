"""This module provides signals for Notification model."""

from datetime import date, datetime

from kombu.exceptions import OperationalError
from celery.exceptions import TaskError
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from utils.tasks import prepare_notification
from utils.utils import LOGGER
from utils.notificationhelper import (get_prepare_task_time,
                                      get_notifications_tasks,
                                      set_notifications_tasks)
from .models import Notification


@receiver(post_delete, sender=Notification)
def revoke_notification_task(sender, instance, **kwargs):  # pylint:disable=unused-argument
    """
    Provides revoking celery appropriate notification
    task and removing data about it from Redis.
    """
    if not instance.week_day == date.today().weekday():
        return False

    notifications_tasks = get_notifications_tasks()

    try:
        celery_task = notifications_tasks.pop(instance.id)
        celery_task.revoke()
    except (KeyError, TaskError) as err:
        LOGGER.error(f'Failed to revoke notification task (id={instance.id}).{err}')
        return False

    if not set_notifications_tasks(notifications_tasks):
        LOGGER.error('Failed to set notifications tasks into redis.')
        return False

    return True


@receiver(post_save, sender=Notification)
def create_notification_task(sender, instance, created, update_fields, **kwargs):  # pylint:disable=unused-argument
    """
    Assign celery task to prepare sending notification or
    revoke old task and assign new one if time was updated.
    """
    instance.refresh_from_db()
    if not instance.is_for_today():
        return False

    notifications_tasks = get_notifications_tasks()

    if not created:
        if 'time' not in update_fields:
            return False

        try:
            celery_task = notifications_tasks.pop(instance.id)
            celery_task.revoke()
        except (KeyError, TaskError) as err:
            LOGGER.error(f'Failed to revoke notification task (id={instance.id}).{err}')
            return False

    now = datetime.now().time()
    if instance.time < now:
        return False

    first_route = instance.way.get_route_by_position(position=0)
    time_to_stop = first_route.time if first_route else None

    task_time = get_prepare_task_time(instance.time, time_to_stop)

    try:
        celery_task = prepare_notification.apply_async(
            eta=task_time,
            kwargs={'notification_id': instance.id}
        )
        notifications_tasks[instance.id] = celery_task
    except(TypeError, OperationalError) as err:
        LOGGER.error(f'Failed to assign task for notification (id={instance.id}).{err}')

    if not set_notifications_tasks(notifications_tasks):
        LOGGER.error('Failed to set notifications tasks into redis.')
        return False

    return True
