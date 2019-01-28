"""This module provides a daemon to work with notifications."""

# pylint: disable=wrong-import-position

import os
import sys
import pickle
from datetime import datetime, timedelta, date

import django
import pytz

SOURCE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SOURCE_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "way_to_home.settings")
django.setup()


from notification.models import Notification
from daemons.base_daemon import Daemon
from utils.redishelper import REDIS_HELPER as redis
from utils.tasks import prepare_notification


DEFAULT_PREPARING_TIME = 60 * 10
KIEV_TZ = pytz.timezone('Europe/Kiev')


def _get_seconds_until_midnight():
    """Return number of seconds until midnight from now."""
    tomorrow = datetime.now() + timedelta(1)
    midnight = tomorrow.replace(hour=0, minute=0, second=0)

    return (midnight - datetime.now()).seconds


class NotifierDaemon(Daemon):
    """
    Daemon class that provides assigning celery tasks to
    parse the arrival time of certain public transport
    before sending a notification to the user.
    """

    def execute(self):
        """
        Defines commands to assign celery tasks to prepare notification
        and insert dictionary with notifications ids and appropriate
        identifiers of planned tasks in Redis in pickled representation.
        """
        today = date.today()
        notification_tasks = {}

        today_notifications = Notification.get_today_scheduled()
        for notification in today_notifications:
            notification_time = datetime.combine(today, notification.time, tzinfo=KIEV_TZ)
            task_time = notification_time - timedelta(seconds=DEFAULT_PREPARING_TIME)

            first_route = notification.way.get_first_route()
            if first_route:
                task_time = task_time - timedelta(
                    hours=first_route.time.hour,
                    minutes=first_route.time.minute,
                    seconds=first_route.time.second
                )

            celery_task = prepare_notification.apply_async(
                eta=task_time,
                kwargs={'notification_id': notification.id}
            )

            notification_tasks[notification.id] = celery_task

        time_until_midnight = _get_seconds_until_midnight()
        redis.set('notifications', pickle.dumps(notification_tasks), cache_time=time_until_midnight)
        self.frequency = time_until_midnight


if __name__ == '__main__':
    NOTIFIER_DAEMON = NotifierDaemon(None)
    NOTIFIER_DAEMON.run()
