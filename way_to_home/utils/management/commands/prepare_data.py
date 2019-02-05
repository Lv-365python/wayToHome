"""This module provides the custom command `prepare_data`."""

from django.core.management.base import BaseCommand

from utils.tasks import prepare_static_easyway_data


class Command(BaseCommand):
    """Custom command to prepare static EasyWay data."""

    help = 'Prepare static data from Easy Way'

    def handle(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Defines commands that handle `prepare_data` custom command."""
        prepare_static_easyway_data.run()
        print('Easy Way data was successfully prepared.')
