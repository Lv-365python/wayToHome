"""This module provides tests for Notifier daemon."""

import logging
from datetime import date, timedelta

from django.test import TestCase
from unittest.mock import patch

from kombu.exceptions import OperationalError

from daemons.notifier_daemon import NotifierDaemon
from notification.models import Notification
from way.models import Way
from custom_user.models import CustomUser


TIME_UNTIL_MIDNIGHT = 24 * 60 * 60


class NotifierDaemonTestCase(TestCase):
    """TestCase for providing Notifier daemon testing."""

    def setUp(self):
        """Provide preparation Notifier daemon testing."""
        logging.disable(logging.INFO)
        logging.disable(logging.ERROR)

        self.notifier_daemon = NotifierDaemon(None)

        user = CustomUser.objects.create(id=100, email='testuser@mail.com', password='testpassword', is_active=True)
        way = Way.objects.create(user=user)
        today = date.today()
        Notification.objects.create(
            id=100,
            way=way,
            start_time=today - timedelta(days=1),
            end_time=today + timedelta(days=31),
            week_day=today.weekday(),
            time='8:30:00'
        )

    def tearDown(self):
        """Provide cleaning commands after Notifier daemon testing."""
        logging.disable(logging.NOTSET)

    def test_daemon_initialization(self):
        """Provide tests for proper initialization of daemon instance."""
        self.assertIsNone(self.notifier_daemon.frequency)
        self.assertIsNone(self.notifier_daemon.pid)
        self.assertFalse(self.notifier_daemon.is_processed)
        self.assertEqual('NotifierDaemon', self.notifier_daemon.name)

    def test_daemon_start(self):
        """Provide tests for proper execution of `start` method."""
        self.notifier_daemon.is_processed = False
        self.notifier_daemon.pid = None

        self.notifier_daemon.start()
        self.assertTrue(self.notifier_daemon.is_processed)
        self.assertIsNotNone(self.notifier_daemon.pid)

    def test_daemon_stop(self):
        """Provide tests for proper execution of `stop` method."""
        self.notifier_daemon.is_processed = True

        self.notifier_daemon.stop()
        self.assertFalse(self.notifier_daemon.is_processed)

    @patch('daemons.notifier_daemon.NotifierDaemon.start')
    @patch('daemons.notifier_daemon.NotifierDaemon.stop')
    @patch('daemons.notifier_daemon.NotifierDaemon.execute')
    def test_daemon_running(self, execute, stop, start):
        """Provide tests for execution of `running` method in case of `is_processed` is False."""
        self.notifier_daemon.is_processed = False

        self.notifier_daemon.run()
        self.assertTrue(start.called)
        self.assertTrue(stop.called)
        self.assertFalse(execute.called)

    @patch('daemons.notifier_daemon.prepare_notification.apply_async')
    @patch('daemons.notifier_daemon.set_notifications_tasks')
    @patch('daemons.notifier_daemon.get_seconds_until_midnight')
    def test_execute_success(self, time_until_midnight, redis_set, assign_task):
        """Provide tests for proper execution of method `execute` method in case of success."""
        time_until_midnight.return_value = TIME_UNTIL_MIDNIGHT
        redis_set.return_value = True
        assign_task.return_value = True

        successful_executed = self.notifier_daemon.execute()
        self.assertTrue(successful_executed)

        expected_frequency = time_until_midnight.return_value
        self.assertEqual(expected_frequency, self.notifier_daemon.frequency)

    @patch('daemons.notifier_daemon.prepare_notification.apply_async')
    @patch('daemons.notifier_daemon.set_notifications_tasks')
    @patch('daemons.notifier_daemon.get_seconds_until_midnight')
    def test_execute_fail_assign_tasks(self, time_until_midnight, redis_set, assign_task):
        """
        Provide tests for proper execution of method `execute`
        method in case of fail celery assigning tasks."""
        time_until_midnight.return_value = TIME_UNTIL_MIDNIGHT
        redis_set.return_value = True

        assign_task.side_effect = TypeError()
        executed = self.notifier_daemon.execute()
        self.assertTrue(executed)

        assign_task.side_effect = OperationalError()
        executed = self.notifier_daemon.execute()
        self.assertTrue(executed)

    @patch('daemons.notifier_daemon.prepare_notification.apply_async', return_value=True)
    @patch('daemons.notifier_daemon.set_notifications_tasks', return_value=False)
    @patch('daemons.notifier_daemon.get_seconds_until_midnight', return_value=TIME_UNTIL_MIDNIGHT)
    def test_execute_fail_redis_set_operation(self, time_until_midnight, redis_set, assign_task):
        """Provide tests for execute method in case of fail Redis set operation."""
        time_until_midnight.return_value = TIME_UNTIL_MIDNIGHT
        redis_set.return_value = False
        assign_task.return_value = True

        successful_executed = self.notifier_daemon.execute()
        self.assertFalse(successful_executed)
