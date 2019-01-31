"""This module provides a daemon to work with notifications."""

# pylint: disable=wrong-import-position

import os
import sys
import django
from kombu.exceptions import OperationalError

SOURCE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SOURCE_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "way_to_home.settings")
django.setup()


from notification.models import Notification
from daemons.base_daemon import Daemon
from utils.tasks import prepare_notification
from utils.utils import LOGGER
from utils.notificationhelper import (get_prepare_task_time,
                                      get_seconds_until_midnight,
                                      set_notifications_tasks)


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
        notifications_tasks = {}

        today_notifications = Notification.get_today_scheduled()
        for notification in today_notifications:
            first_route = notification.way.get_first_route()
            time_to_stop = first_route.time if first_route else None
            task_time = get_prepare_task_time(notification.time, time_to_stop)

            try:
                celery_task = prepare_notification.apply_async(
                    eta=task_time,
                    kwargs={'notification_id': notification.id}
                )
                notifications_tasks[notification.id] = celery_task
            except(TypeError, OperationalError) as err:
                LOGGER.error(f'Failed to assign task for notification (id={notification.id}).{err}')

        self.frequency = get_seconds_until_midnight()
        if not set_notifications_tasks(notifications_tasks):
            LOGGER.error('Failed to set notifications tasks into redis.')
            return False

        return True


if __name__ == '__main__':
    NOTIFIER_DAEMON = NotifierDaemon(None)
    NOTIFIER_DAEMON.run()
