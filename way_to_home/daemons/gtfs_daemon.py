"""This module provides daemon to work with GTFS data."""

# pylint: disable=wrong-import-position

import os
import pickle
import sys
import django


SOURCE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SOURCE_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "way_to_home.settings")
django.setup()


from django.conf import settings
from utils.file_handlers import load_file
from utils.easy_way import compile_file
from utils.redishelper import REDIS_HELPER as redis
from utils.utils import LOGGER
from daemons.base_daemon import Daemon
from daemons.helper import parse_args


class GTFSDaemon(Daemon):
    """Daemon class that provides preparing GTFS data from EasyWay."""

    def execute(self):
        """
        Defines commands to download file with data about Lviv
        transport geolocation, compile the loaded file and insert
        parsed necessary data into Redis in pickled representation.
        """
        url = 'http://track.ua-gis.com/gtfs/lviv/vehicle_position'
        redis_gtfs_key = 'gtfs_data'

        loaded_file = load_file(url, save_to=settings.EASY_WAY_DIR)
        if not loaded_file:
            LOGGER.info(f'Unsuccessful gtfs data file load')
            return False

        gtfs_data = compile_file(loaded_file)
        if not gtfs_data:
            LOGGER.info(f'Unsuccessful compilation of gtfs data file.')
            return False

        gtfs_data = pickle.dumps(gtfs_data)
        if not redis.set(redis_gtfs_key, gtfs_data):
            LOGGER.info(f'Unsuccessful sets gtfs data in redis.')
            return False

        return True


if __name__ == '__main__':
    FREQUENCY = parse_args()
    GTFS_DAEMON = GTFSDaemon(FREQUENCY)
    GTFS_DAEMON.run()
