"""This module provides signals for Notification model."""

import pickle

from django.db.models.signals import post_delete
from django.dispatch import receiver

from utils.redishelper import REDIS_HELPER as redis
from .models import Notification


@receiver(post_delete, sender=Notification)
def revoke_notification_task(sender, instance, **kwargs):  # pylint:disable=unused-argument
    """
    Provides revoking celery appropriate notification
    task and removing data about it from Redis.
    """
    pickled_notifications = redis.get('notifications')
    notifications = pickle.loads(pickled_notifications)
    celery_task = notifications.pop(instance.id)

    celery_task.revoke()

    redis.set('notifications', pickle.dumps(notifications))
