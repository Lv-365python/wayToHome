"""This module provides celery tasks."""

import pickle

from celery.schedules import crontab
from celery.task import periodic_task, task

from django.conf import settings
from notification.models import Notification
from utils.utils import LOGGER
from .file_handlers import load_file, unzip_file
from .redishelper import REDIS_HELPER as redis
from .easy_way import parse_routes_data, parse_trips_data, parse_stops_data


DEFAULT_RETRY_DELAY = 60
CLEANER_CTONTAB = crontab(hour=1, minute=30)
EASYWAY_CTONTAB = crontab(hour=2, day_of_week=1)
EASYWAY_DIR = settings.EASY_WAY_DIR
EASYWAY_PARSERS = {
    'stops': parse_stops_data,
    'routes': parse_routes_data,
    'trips': parse_trips_data
}


@periodic_task(bind=True,
               name='delete expired notifications',
               run_every=CLEANER_CTONTAB,
               default_retry_delay=DEFAULT_RETRY_DELAY)
def delete_expired_notifications(self):
    """Delete notifications that have expired datetime every day at 1:30 a.m."""
    retry = False

    notifications = Notification.get_expired()
    for notification_id in notifications.values_list('id', flat=True):
        if not Notification.delete_by_id(obj_id=notification_id):
            LOGGER.info(f'Notification with {self.notification_id} doesn\'t delete')
            retry = True

    if retry:
        raise self.retry()


@periodic_task(bind=True,
               name='prepare static easy way data',
               run_every=EASYWAY_CTONTAB,
               default_retry_delay=DEFAULT_RETRY_DELAY)
def prepare_static_easyway_data(self):
    """
    Provide preparing static data from EasyWay every Monday at 2 a.m.
    Defines commands to download static files, unzip it, parse necessary data
    from appropriate files and insert it into Redis in pickled representation.
    """
    url = 'http://track.ua-gis.com/gtfs/lviv/static.zip'

    loaded_file = load_file(url, save_to=EASYWAY_DIR)
    if not loaded_file:
        LOGGER.info('File doesn\'t load.')
        raise self.retry()

    is_unzipped = unzip_file(loaded_file, unzip_to=EASYWAY_DIR)
    if not is_unzipped:
        LOGGER.info('File doesn\'t unzip.')
        raise self.retry()

    for data_identifier, parser in EASYWAY_PARSERS.items():
        file_path = f'{EASYWAY_DIR}/{data_identifier}.txt'
        parsed_data = parser(file_path)
        pickled_data = pickle.dumps(parsed_data)
        redis.set(data_identifier, pickle.dumps(pickled_data))


@task
def prepare_notification(notification_id):  # pylint: disable=unused-argument
    """Prepare data about transport arrival time before notifying the user."""
