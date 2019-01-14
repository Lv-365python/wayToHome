"""This module provides daemon for preparing gtfs data from EasyWay."""

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
from base_daemon import Daemon
from helper import parse_args


class GTFSDaemon(Daemon):
    """Daemon class that provides preparing GTFS data from EasyWay."""

    def execute(self):
        """Defines commands for preparing GTFS data from EasyWay."""
        url = f'http://track.ua-gis.com/gtfs/lviv/vehicle_position'

        loaded_file = load_file(url, save_to=settings.EASY_WAY_DIR)
        if not loaded_file:
            return False

        gtfs_data = compile_file(loaded_file)
        if not gtfs_data:
            return False

        gtfs_data = pickle.dumps(gtfs_data)  # FIXME: deep pickling
        if not redis.set('gtfs_data', gtfs_data, 11):  # FIXME: expire time
            return False

        return True


if __name__ == '__main__':
    FREQUENCY = parse_args()
    GTFS_DAEMON = GTFSDaemon(FREQUENCY)
    GTFS_DAEMON.run()
