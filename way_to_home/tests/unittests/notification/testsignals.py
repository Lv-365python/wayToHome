"""This module provides tests for Notifications signals."""

import logging
from datetime import date, timedelta, time, datetime

from kombu.exceptions import OperationalError
from celery.exceptions import TaskError
from celery.result import AsyncResult
from django.db.models import signals
from django.test import TestCase
from unittest.mock import patch

from custom_user.models import CustomUser
from notification.models import Notification
from notification.signals import revoke_notification_task, create_notification_task
from way.models import Way


class NotificationSignalsTestCase(TestCase):
    """TestCase for providing Notification signals testing."""

    def setUp(self):
        """Method that provides preparation before testing Notification signals."""
        logging.disable(logging.INFO)
        logging.disable(logging.ERROR)

        signals.post_save.disconnect(create_notification_task, sender=Notification)
        signals.post_delete.disconnect(revoke_notification_task, sender=Notification)

        today = date.today()

        user = CustomUser.objects.create(id=100, email='testuser@mail.com', password='testpassword', is_active=True)
        way = Way.objects.create(id=100, user=user)
        self.notification = Notification.objects.create(
            id=100,
            way=way,
            start_time=today - timedelta(days=1),
            end_time=today + timedelta(days=1),
            week_day=today.weekday(),
            time=time(23, 59, 59)
        )
        self.post_save_params = {
            'sender': Notification,
            'instance': self.notification,
            'created': True,
            'update_fields': []
        }
        self.notifications_tasks = {self.notification.id: AsyncResult(self.notification.id)}

    def tearDown(self):
        """Provide cleaning commands after Notifications signals testing."""
        logging.disable(logging.NOTSET)

        signals.post_save.connect(create_notification_task, sender=Notification)
        signals.post_delete.connect(revoke_notification_task, sender=Notification)

    @patch('celery.result.AsyncResult.revoke')
    @patch('notification.signals.set_notifications_tasks')
    @patch('notification.signals.get_notifications_tasks')
    def test_revoke_notification_success(self, get_notifications_tasks, set_notifications_tasks, revoke_task):
        """Provide tests for proper execution of post delete callback function in case of success."""
        get_notifications_tasks.return_value = self.notifications_tasks
        set_notifications_tasks.return_value = True
        revoke_task.return_value = True

        successful_executed = revoke_notification_task(Notification, self.notification)
        self.assertTrue(successful_executed)

    def test_revoke_notification_task_another_weekday(self):
        """
        Provide tests for proper execution of post delete callback
        function in case of notification weekday is not relevant.
        """
        self.notification.week_day = 100

        successful_executed = revoke_notification_task(Notification, self.notification)
        self.assertFalse(successful_executed)

    @patch('notification.signals.get_notifications_tasks')
    def test_revoke_notification_task_key_error(self, get_notifications_tasks):
        """
        Provide tests for proper execution of post delete callback function
        in case of notification`s data doesn't exist in Redis.
        """
        get_notifications_tasks.return_value = {}

        successful_executed = revoke_notification_task(Notification, self.notification)
        self.assertFalse(successful_executed)

    @patch('celery.result.AsyncResult.revoke')
    @patch('notification.signals.get_notifications_tasks')
    def test_revoke_notification_task_revoke_error(self, get_notifications_tasks, revoke_task):
        """
        Provide tests for proper execution of post delete callback
        function in case of celery revoke task is failed.
        """
        get_notifications_tasks.return_value = self.notifications_tasks
        revoke_task.side_effect = TaskError()

        successful_executed = revoke_notification_task(Notification, self.notification)
        self.assertFalse(successful_executed)

    @patch('celery.result.AsyncResult.revoke')
    @patch('notification.signals.set_notifications_tasks')
    @patch('notification.signals.get_notifications_tasks')
    def test_revoke_notification_task_set_error(self, get_notifications_tasks,
                                                set_notifications_tasks, revoke_task):
        """
        Provide tests for proper execution of post delete callback
        function in case of fail Redis set operation.
        """
        get_notifications_tasks.return_value = self.notifications_tasks
        set_notifications_tasks.return_value = False
        revoke_task.return_value = True

        successful_executed = revoke_notification_task(Notification, self.notification)
        self.assertFalse(successful_executed)

    @patch('celery.result.AsyncResult.revoke')
    @patch('utils.tasks.prepare_notification.apply_async')
    @patch('notification.signals.set_notifications_tasks')
    @patch('notification.signals.get_notifications_tasks')
    def test_create_notification_task_success_after_create(self, get_notifications_tasks,
                                                           set_notifications_tasks,
                                                           assign_task, revoke_task):
        """Provide tests for proper execution of post save callback function in case success."""
        get_notifications_tasks.return_value = self.notifications_tasks
        set_notifications_tasks.return_value = True
        assign_task.return_value = True

        successful_executed = create_notification_task(**self.post_save_params)
        self.assertTrue(successful_executed)

    @patch('celery.result.AsyncResult.revoke')
    @patch('utils.tasks.prepare_notification.apply_async')
    @patch('notification.signals.set_notifications_tasks')
    @patch('notification.signals.get_notifications_tasks')
    def test_create_notification_task_success_after_update(self, get_notifications_tasks,
                                                           set_notifications_tasks,
                                                           assign_task, revoke_task):
        """Provide tests for proper execution of post update callback function in case success."""
        post_save_params = self.post_save_params.copy()
        post_save_params['created'] = False
        post_save_params['update_fields'] = ['time']

        get_notifications_tasks.return_value = self.notifications_tasks
        set_notifications_tasks.return_value = True
        assign_task.return_value = True
        revoke_task.return_value = True

        successful_executed = create_notification_task(**post_save_params)
        self.assertTrue(successful_executed)

    @patch('notification.models.Notification.is_for_today')
    def test_create_notification_task_invalid_date(self, is_for_today):
        """
        Provide tests for proper execution of post save callback
        function in case of notification date data is not relevant.
        """
        is_for_today.return_value = False

        successful_executed = create_notification_task(**self.post_save_params)
        self.assertFalse(successful_executed)

    @patch('notification.signals.get_notifications_tasks')
    def test_create_notification_task_time_not_updated(self, get_notifications_tasks):
        """
        Provide tests for proper execution of post save callback
        function in case of notification time field was not updated.
        """
        post_save_params = self.post_save_params.copy()
        post_save_params['created'] = False
        get_notifications_tasks.return_value = {}

        successful_executed = create_notification_task(**post_save_params)
        self.assertFalse(successful_executed)

    @patch('notification.signals.get_notifications_tasks')
    def test_create_notification_task_key_error(self, get_notifications_tasks):
        """
        Provide tests for proper execution of post save callback function
        in case of notification`s data doesn't exist in Redis.
        """
        post_save_params = self.post_save_params.copy()
        post_save_params['update_fields'] = ['time']
        post_save_params['created'] = False
        get_notifications_tasks.return_value = {}

        successful_executed = create_notification_task(**post_save_params)
        self.assertFalse(successful_executed)

    @patch('celery.result.AsyncResult.revoke')
    @patch('notification.signals.get_notifications_tasks')
    def test_create_notification_task_revoke_error(self, get_notifications_tasks, revoke_task):
        """
        Provide tests for proper execution of post save callback
        function in case of celery revoke old task is failed.
        """
        post_save_params = self.post_save_params.copy()
        post_save_params['update_fields'] = ['time']
        post_save_params['created'] = False

        get_notifications_tasks.return_value = self.notifications_tasks
        revoke_task.side_effect = TaskError()

        successful_executed = create_notification_task(**post_save_params)
        self.assertFalse(successful_executed)

    @patch('notification.signals.get_notifications_tasks')
    def test_create_notification_task_invalid_time(self, get_notifications_tasks):
        """
        Provide tests for proper execution of post save callback
        function in case of notification is not relevant for today.
        """
        get_notifications_tasks.return_value = self.notifications_tasks
        self.notification.time = datetime.now() - timedelta(seconds=1)
        self.notification.save()

        successful_executed = create_notification_task(**self.post_save_params)
        self.assertFalse(successful_executed)

    @patch('utils.tasks.prepare_notification.apply_async')
    @patch('notification.signals.set_notifications_tasks')
    @patch('notification.signals.get_notifications_tasks')
    def test_create_notification_task_assign_error(self, get_notifications_tasks,
                                                   set_notifications_tasks, assign_task):
        """
        Provide tests for proper execution of post save callback
        function in case of celery assign task is failed.
        """
        get_notifications_tasks.return_value = self.notifications_tasks
        set_notifications_tasks.return_value = True

        assign_task.side_effect = TypeError()
        executed = create_notification_task(**self.post_save_params)
        self.assertTrue(executed)

        assign_task.side_effect = OperationalError()
        executed = create_notification_task(**self.post_save_params)
        self.assertTrue(executed)

    @patch('utils.tasks.prepare_notification.apply_async')
    @patch('notification.signals.set_notifications_tasks')
    @patch('notification.signals.get_notifications_tasks')
    def test_create_notification_task_set_error(self, get_notifications_tasks,
                                                set_notifications_tasks, assign_task):
        """
        Provide tests for proper execution of post save callback
        function in case of Redis set operation is failed.
        """
        get_notifications_tasks.return_value = self.notifications_tasks
        set_notifications_tasks.return_value = False
        assign_task.return_value = True

        successful_executed = create_notification_task(**self.post_save_params)
        self.assertFalse(successful_executed)
