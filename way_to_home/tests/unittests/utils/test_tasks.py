"""This module provides tests for Celery tasks."""

import datetime

from unittest.mock import patch
from django.test import TestCase
from django.db.models import signals
from celery.exceptions import Retry

from custom_user.models import CustomUser
from notification.models import Notification
from notification.signals import create_notification_task, revoke_notification_task
from way.models import Way
from utils.tasks import delete_expired_notifications, prepare_static_easyway_data

MOCK_EASYWAY_PARSERS = {
    'stops': lambda file_path: 'parsed stops',
    'routes': lambda file_path: 'parsed routes',
    'trips': lambda file_path: 'parsed trips'
}


class CeleryTasksTestCase(TestCase):
    """TestCase for providing Celery tasks testing."""

    def setUp(self):
        """Provide preparation before testing Celery tasks."""
        signals.post_save.disconnect(create_notification_task, sender=Notification)
        signals.post_delete.disconnect(revoke_notification_task, sender=Notification)

        user = CustomUser.objects.create(id=100, email='testuser@mail.com', password='testpassword')
        way = Way.objects.create(id=100, user=user)

        today = datetime.date.today()
        self.expired_notification = Notification.objects.create(
            id=100,
            way=way,
            start_time=today - datetime.timedelta(days=31),
            end_time=today - datetime.timedelta(days=1),
            week_day=1,
            time='8:30:00'
        )

    def test_delete_expired_notification_success(self):
        """Provide tests for `delete_expired_notifications` Celery periodic task in case of success."""
        successful_deleted = delete_expired_notifications.run()

        self.assertTrue(successful_deleted)
        self.assertRaises(Notification.DoesNotExist,
                          Notification.objects.get,
                          id=self.expired_notification.id)

    @patch('utils.tasks.Notification.delete_by_id')
    def test_delete_expired_notification_fail_delete(self, mock_delete_by_id):
        """
        Provide tests for `delete_expired_notifications` Celery periodic
        task in case of notification delete operation was failed.
        """
        mock_delete_by_id.return_value = False
        self.assertRaises(Retry, delete_expired_notifications.run)

    @patch('utils.tasks.load_file')
    def test_prepare_static_easyway_data_fail_load(self, mock_load_file):
        """Provide tests for `prepare_static_easyway_data` in case of load operation was failed."""
        mock_load_file.return_value = None
        self.assertRaises(Retry, prepare_static_easyway_data.run)

    @patch('utils.tasks.load_file')
    @patch('utils.tasks.unzip_file')
    def test_prepare_static_easyway_data_fail_unzip(self, mock_unzip_file, mock_load_file):
        """Provide tests for `prepare_static_easyway_data` in case of unzip operation was failed."""
        mock_load_file.return_value = 'loaded file'
        mock_unzip_file.return_value = False

        self.assertRaises(Retry, prepare_static_easyway_data.run)

    @patch('utils.tasks.EASYWAY_PARSERS', MOCK_EASYWAY_PARSERS)
    @patch('utils.tasks.load_file')
    @patch('utils.tasks.unzip_file')
    @patch('utils.tasks.REDIS_HELPER.set')
    def test_prepare_static_easyway_data_fail_success(self, mock_redis_set,
                                                      mock_unzip_file, mock_load_file):
        """Provide tests for `prepare_static_easyway_data` in case of success."""
        mock_load_file.return_value = 'loaded file'
        mock_unzip_file.return_value = True
        mock_redis_set.return_value = True

        successful_prepared = prepare_static_easyway_data.run()
        self.assertTrue(successful_prepared)
