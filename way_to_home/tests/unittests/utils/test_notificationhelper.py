"""
Notification helper test
========================
This module provides complete testing for all notification functions.
"""

import pytz
import pickle
from celery.result import AsyncResult
from freezegun import freeze_time
from unittest import mock
from datetime import datetime, date, timedelta, time
from django.test import TestCase

from utils.notificationhelper import (get_seconds_until_midnight,
                                     get_prepare_task_time,
                                     set_notifications_tasks,
                                     get_notifications_tasks,
                                     )


class NotificationTestCase(TestCase):
    """TestCase for providing functions of notification testing"""

    def setUp(self):
        """Provide preparation NotificationHelper testing."""
        kiev_tz = pytz.timezone('Europe/Kiev')
        today = date.today()
        self.notification_time = time(10, 0, 0)
        self.preparing_time = 60 * 10
        notification_datetime = datetime.combine(today, self.notification_time, tzinfo=kiev_tz)
        self.task_time = notification_datetime - timedelta(seconds=self.preparing_time)

    @freeze_time('2019-01-01-10-30-00')
    def test_get_seconds_until_midnight(self):
        """Provide tests for `get_seconds_until_midnight` method."""
        tomorrow = datetime.now() + timedelta(days=1)
        midnight = tomorrow.replace(hour=0, minute=0, second=0)
        expected_time = (midnight - datetime.now()).seconds
        gotten_time = get_seconds_until_midnight()
        self.assertEqual(expected_time, gotten_time)

    @mock.patch('utils.redishelper.REDIS_HELPER.get')
    def test_get_notifications_tasks_if_nonexistent(self, redis_get):
        """Provide tests for `get_notifications_tasks` method
        in case if notification task not exist."""
        redis_get.return_value = None
        gotten_result = get_notifications_tasks()
        self.assertDictEqual(gotten_result, {})

    @mock.patch('utils.redishelper.REDIS_HELPER.get')
    def test_get_notifications_tasks(self, redis_get):
        """Provide tests for `get_notifications_tasks` method."""
        notification_id = 100
        notifications_tasks = {notification_id: AsyncResult(notification_id)}
        redis_get.return_value = pickle.dumps(notifications_tasks)
        gotten_result = get_notifications_tasks()
        self.assertDictEqual(gotten_result, notifications_tasks)

    @mock.patch('utils.notificationhelper.get_seconds_until_midnight')
    @mock.patch('utils.redishelper.REDIS_HELPER.set')
    def test_set_notifications_tasks(self, redis_set, get_seconds_until_midnight):
        """Provide tests for `set_notifications_tasks` method."""
        redis_set.return_value = True
        expected_result = set_notifications_tasks({'test_key': 'test_value'})
        self.assertTrue(get_seconds_until_midnight.called)
        self.assertTrue(redis_set.called)
        self.assertTrue(expected_result)

        redis_set.return_value = False
        expected_result = set_notifications_tasks({'test_key': 'test_value'})
        self.assertTrue(get_seconds_until_midnight.called)
        self.assertTrue(redis_set.called)
        self.assertFalse(expected_result)

    def test_get_prepare_task_time(self):
        """Provide tests for `get_prepare_task_time` method."""
        time_to_stop = time(10, 15, 30)
        task_time = self.task_time - timedelta(
            hours=time_to_stop.hour,
            minutes=time_to_stop.minute,
            seconds=time_to_stop.second
        )
        expected_task_time = task_time
        gotten_task_time = get_prepare_task_time(
            self.notification_time,
            time_to_stop,
            self.preparing_time
        )
        self.assertEqual(expected_task_time, gotten_task_time)

    def test_get_prepare_task_time_if_time_to_stop_none(self):
        """Provide tests for `get_prepare_task_time` method in the case when
            `time_to_stop` parameter not exist."""
        time_to_stop = None
        expected_task_time = self.task_time
        gotten_task_time = get_prepare_task_time(
            self.notification_time,
            time_to_stop,
            self.preparing_time
        )
        self.assertEqual(expected_task_time, gotten_task_time)
