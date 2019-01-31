"""This module provides helper functionality to work with notifications."""

import pickle
from datetime import datetime, date, timedelta

import pytz

from .redishelper import REDIS_HELPER


KIEV_TZ = pytz.timezone('Europe/Kiev')
DEFAULT_PREPARING_TIME = 60 * 10
NOTIFICATIONS_TASKS_KEY = 'notifications'


def get_seconds_until_midnight():
    """Return number of seconds until midnight from now."""
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    midnight = tomorrow.replace(hour=0, minute=0, second=0)

    return (midnight - today).seconds


def get_notifications_tasks():
    """Retrieve dictionary with data about notifications tasks from Redis."""
    pickled_notifications = REDIS_HELPER.get(NOTIFICATIONS_TASKS_KEY)
    if not pickled_notifications:
        return {}

    notifications_tasks = pickle.loads(pickled_notifications)
    return notifications_tasks


def set_notifications_tasks(notifications_tasks):
    """Set pickled dictionary with data about notification tasks to Redis."""
    cache_time = get_seconds_until_midnight()
    inserted = REDIS_HELPER.set(
        NOTIFICATIONS_TASKS_KEY,
        pickle.dumps(notifications_tasks),
        cache_time=cache_time
    )

    return inserted


def get_prepare_task_time(notification_time, time_to_stop=None,
                          preparing_time=DEFAULT_PREPARING_TIME):
    """
    Return a time at which need to assign the task
    to begin preparing data to send notifications.
    """
    today = date.today()
    notification_time = datetime.combine(today, notification_time, tzinfo=KIEV_TZ)
    task_time = notification_time - timedelta(seconds=preparing_time)

    if time_to_stop:
        task_time = task_time - timedelta(
            hours=time_to_stop.hour,
            minutes=time_to_stop.minute,
            seconds=time_to_stop.second
        )

    return task_time
