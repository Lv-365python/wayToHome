"""This module provides tests for Celery tasks."""

import datetime

from unittest.mock import patch
from django.test import TestCase
from django.db.models import signals
from celery.exceptions import Retry

from custom_user.models import CustomUser
from notification.models import Notification
from notification.signals import create_notification_task, revoke_notification_task
from place.models import Place
from route.models import Route
from user_profile.models import UserProfile
from way.models import Way
from utils.tasks import (delete_expired_notifications,
                         prepare_static_easyway_data,
                         send_notification,
                         prepare_notification)

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

        self.user = CustomUser.objects.create(id=100,
                                              email='testuser@mail.com',
                                              password='testpassword',
                                              phone_number='+380111111111')
        self.user_profile = UserProfile.objects.create(id=100, user=self.user)
        way = Way.objects.create(id=100, user=self.user)
        point_A = Place.objects.create(longitude=43.1234, latitude=34.1234)
        point_B = Place.objects.create(longitude=43.1234, latitude=34.1234)
        route = Route.objects.create(way=way,
                                     start_place=point_A,
                                     end_place=point_B,
                                     time='08:30:00',
                                     position=1)

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

    @patch('utils.tasks.send_telegram_message')
    @patch('utils.tasks.send_sms')
    def test_send_notification_success(self, mock_send_sms, mock_send_telegram_message):
        """Provide tests for `send_notification` task in case of success."""
        mock_send_sms.return_value = True

        successful_sent = send_notification.run(user_id=self.user.id,
                                                arriving_time=10, route_name='A45')
        self.assertTrue(successful_sent)

        mock_send_telegram_message.return_value = True
        self.user_profile.telegram_id = 100
        self.user_profile.save()

        successful_sent = send_notification.run(user_id=self.user.id,
                                                arriving_time=10, route_name='A45')
        self.assertTrue(successful_sent)

    @patch('utils.tasks.send_telegram_message')
    @patch('utils.tasks.send_sms')
    def test_send_notification_fail(self, mock_send_sms, mock_send_telegram_message):
        """Provide tests for `send_notification` task in case of send operation was failed."""
        mock_send_sms.return_value = False

        self.assertRaises(Retry, send_notification.run,
                          user_id=self.user.id, arriving_time=10, route_name='A45')

        mock_send_telegram_message.return_value = False
        self.user_profile.telegram_id = 100
        self.user_profile.save()

        self.assertRaises(Retry, send_notification.run,
                          user_id=self.user.id, arriving_time=10, route_name='A45')

    @patch('pickle.loads')
    @patch('utils.tasks.get_route_id_by_name')
    @patch('utils.tasks.REDIS_HELPER.get')
    def test_prepare_notification_fail_route_id(self, mock_redis_get, mock_route_id, mock_pickle_loads):
        """Provide tests for `prepare_notification` task in case of route id equals `None`."""
        mock_redis_get.return_value = 'data from redis'
        mock_pickle_loads.return_value = 'unpickled data'
        mock_route_id.return_value = None

        successful_prepared = prepare_notification.run(self.expired_notification.id)
        self.assertFalse(successful_prepared)
        self.assertTrue(mock_redis_get)
        self.assertTrue(mock_pickle_loads)
        self.assertTrue(mock_route_id)

    @patch('pickle.loads')
    @patch('utils.tasks.get_route_id_by_name')
    @patch('utils.tasks.REDIS_HELPER.get')
    def test_prepare_notification_fail_buses(self, mock_redis_get, mock_route_id, mock_pickle_loads):
        """Provide tests for `prepare_notification` task in case of buses equals `None`."""
        mock_redis_get.return_value = 'data from redis'
        mock_pickle_loads.return_value = {10: 'first route data', 20: 'second route data'}
        mock_route_id.return_value = '100'

        successful_prepared = prepare_notification.run(self.expired_notification.id)
        self.assertFalse(successful_prepared)
        self.assertTrue(mock_redis_get)
        self.assertTrue(mock_pickle_loads)
        self.assertTrue(mock_route_id)

    @patch('pickle.loads')
    @patch('utils.tasks.get_route_id_by_name')
    @patch('utils.tasks.REDIS_HELPER.get')
    @patch('utils.tasks.find_closest_bus_time')
    @patch('utils.tasks.send_notification.delay')
    def test_prepare_notification_success(self, mock_delay_task, mock_find_time, mock_redis_get,
                                          mock_route_id, mock_pickle_loads):
        """Provide tests for `prepare_notification` task in case of success."""
        mock_redis_get.return_value = 'data from redis'
        mock_find_time.return_value = 60 * 5
        mock_delay_task.return_value = True
        mock_route_id.return_value = '100'
        mock_pickle_loads.return_value = {'100': [{'trip_id': '1085_0_0',
                                                   'lat': 49.80695724487305,
                                                   'lon': 24.0104408264160}]
                                          }

        successful_prepared = prepare_notification.run(self.expired_notification.id)
        self.assertTrue(successful_prepared)
        self.assertTrue(mock_redis_get)
        self.assertTrue(mock_pickle_loads)
        self.assertTrue(mock_route_id)
        self.assertTrue(mock_delay_task)
        self.assertTrue(mock_find_time)
