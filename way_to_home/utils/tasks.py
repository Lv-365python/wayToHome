"""This module provides celery tasks."""

import pickle
import time

from celery.schedules import crontab
from celery.task import periodic_task, task

from django.conf import settings

from custom_user.models import CustomUser
from notification.models import Notification
from way.models import Way
from .notificationhelper import get_route_id_by_name
from .utils import LOGGER
from .file_handlers import load_file, unzip_file
from .redishelper import REDIS_HELPER
from .easy_way import parse_routes_data, parse_trips_data, parse_stops_data, prettify_gtfs
from .mapshelper import find_closest_bus_time
from .senderhelper import send_sms, send_telegram_message


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
            LOGGER.error(f'Expired notification with id={notification_id} was not deleted')
            retry = True

    if retry:
        raise self.retry()

    LOGGER.info('Expired notifications was successfully deleted')
    return True


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
        LOGGER.error('File with static data was not loaded from EasyWay')
        raise self.retry()

    is_unzipped = unzip_file(loaded_file, unzip_to=EASYWAY_DIR)
    if not is_unzipped:
        LOGGER.error('File with static data was not unzipped')
        raise self.retry()

    for data_identifier, parser in EASYWAY_PARSERS.items():
        file_path = f'{EASYWAY_DIR}/{data_identifier}.txt'
        parsed_data = parser(file_path)
        pickled_data = pickle.dumps(parsed_data)
        REDIS_HELPER.set(data_identifier, pickled_data)

    LOGGER.info('EasyWay static data was successfully prepared')
    return True


@task
def prepare_notification(notification_id):
    """Prepare data about transport arrival time before notifying the user."""
    way = Way.get_by_notification(notification_id)

    route = way.get_route_by_position(position=1)
    route_name = route.transport_name
    bus_stop = route.start_place
    stop_coords = f'{bus_stop.latitude},{bus_stop.longitude}'

    pickled_routes_data = REDIS_HELPER.get('routes')
    routes_data = pickle.loads(pickled_routes_data)
    route_id = get_route_id_by_name(routes_data, route_name)
    if not route_id:
        LOGGER.error(f'Failed to find route with name={route_name} from routes data')
        return False

    gtfs_data = pickle.loads(REDIS_HELPER.get('gtfs_data'))
    buses = gtfs_data.get(route_id)
    if not buses:
        LOGGER.error(f'Failed to retrieve route with id={route_id} from GTFS data')
        return False

    buses_coords = prettify_gtfs(buses)
    bus_time = find_closest_bus_time(buses_coords, stop_coords)
    arriving_time = int(time.strftime("%M", time.gmtime(bus_time)))

    send_notification.delay(way.user_id, arriving_time)

    LOGGER.info(f'Notification with id={notification_id} was successfully prepared')
    return True


@task(bind=True, retry_kwargs={'max_retries': 5})
def send_notification(self, user_id, arriving_time):
    """Send notification about transport arrival."""
    user = CustomUser.get_by_id(user_id)
    message = f'Ваш транспорт прибуде через {arriving_time} хвилин'
    was_sent = False

    chat_id = user.user_profile.telegram_id
    phone_number = user.phone_number

    if chat_id:
        was_sent = send_telegram_message(chat_id, message)
    elif phone_number:
        was_sent = send_sms(phone_number, message)

    if not was_sent:
        LOGGER.error(f'Notification was not sent to user with id={user_id}')
        raise self.retry(countdown=5)

    LOGGER.info(f'Notification was successfully prepared sent to user with id={user_id}')
    return was_sent
