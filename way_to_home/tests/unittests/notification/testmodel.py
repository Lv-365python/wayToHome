"""This module provides tests for Notification model."""

import datetime

from django.test import TestCase

from custom_user.models import CustomUser
from notification.models import Notification
from way.models import Way


class NotificationModelTestCase(TestCase):
    """TestCase for providing Notification model testing."""

    def setUp(self):
        """Method that provides preparation before testing Notification model's features."""
        user = CustomUser.objects.create(id=100, email='testuser@mail.com', password='testpassword', is_active=True)
        self.way = Way.objects.create(id=100, user=user)
        self.notification = Notification.objects.create(
            id=100,
            way=self.way,
            start_time=datetime.date(2019, 10, 29),
            end_time=datetime.date(2019, 12, 29),
            week_day=6,
            time=datetime.time(23, 58, 59)
        )

    def test_get_by_id(self):
        """Provide tests for `get_by_id` method of certain Notification instance."""
        expected_notification = Notification.objects.get(id=self.notification.id)
        actual_notification = Notification.get_by_id(obj_id=self.notification.id)
        self.assertEqual(expected_notification, actual_notification)

        unexisting_notification = Notification.get_by_id(obj_id=999)
        self.assertIsNone(unexisting_notification)
        self.assertRaises(Notification.DoesNotExist, Notification.objects.get, id=999)

    def test_delete_by_id(self):
        """Provide tests for `delete_by_id` method of certain Notification instance."""
        is_deleted = Notification.delete_by_id(obj_id=self.notification.id)
        self.assertTrue(is_deleted)
        self.assertRaises(Notification.DoesNotExist, Notification.objects.get, id=self.notification.id)

        is_deleted = Notification.delete_by_id(obj_id=999)
        self.assertFalse(is_deleted)

    def test_to_dict(self):
        """Provide tests for `to_dict` method of certain Notification instance."""
        notification = Notification.objects.get(id=self.notification.id)

        expected_dict = {
            'id': 100,
            'start_time': datetime.date(2019, 10, 29),
            'end_time': datetime.date(2019, 12, 29),
            'week_day': 6,
            'time': datetime.time(23, 58, 59),
            'way': 100
        }

        actual_dict = notification.to_dict()
        self.assertDictEqual(expected_dict, actual_dict)

    def test_str(self):
        """Provide tests for `__str__` method of certain Notification instance."""
        notification = Notification.objects.get(id=self.notification.id)

        expected_string = 'notification at: 6 23:58:59'
        actual_string = notification.__str__()

        self.assertEqual(expected_string, actual_string)

    def test_create(self):
        """Provide tests for `create` method of Notification model."""
        start_date = datetime.date(2019, 10, 29)
        end_date = datetime.date(2019, 12, 29)

        notification = Notification.create(
            way=self.way,
            start_time=start_date,
            end_time=end_date,
            week_day=6,
            time='23:58:59'
        )

        self.assertIsInstance(notification, Notification)
        self.assertIsNotNone(Notification.objects.get(id=notification.id))

        notification = Notification.create(way=Way(), start_time='', end_time='', week_day=-1, time='')
        self.assertIsNone(notification)

    def test_update(self):
        """Provide tests for `update` method of certain Notification instance."""
        new_time = datetime.time(1, 2, 3)
        new_week_day = 2
        is_updated = self.notification.update(time=new_time, week_day=new_week_day)
        self.assertTrue(is_updated)

        notification = Notification.objects.get(id=self.notification.id)
        self.assertEqual(notification.week_day, new_week_day)
        self.assertEqual(notification.time, new_time)

        new_week_day = -1
        is_updated = self.notification.update(week_day=new_week_day)
        self.assertFalse(is_updated)
        notification = Notification.objects.get(id=self.notification.id)
        self.assertNotEqual(notification.week_day, new_week_day)

    def test_get_expired(self):
        """Provides tests for `get_expired` method."""
        today = datetime.date.today()

        expired_notification = Notification.objects.create(
            id=201,
            way=self.way,
            start_time=today - datetime.timedelta(days=31),
            end_time=today - datetime.timedelta(days=1),
            week_day=1,
            time='8:30:00'
        )
        relevant_notification = Notification.objects.create(
            id=202,
            way=self.way,
            start_time=today - datetime.timedelta(days=31),
            end_time=today + datetime.timedelta(days=1),
            week_day=1,
            time='8:30:00'
        )

        expected_query = Notification.objects.filter(end_time__lt=today)
        actual_query = Notification.get_expired()

        self.assertQuerysetEqual(actual_query, expected_query, transform=lambda x: x)
        self.assertIn(expired_notification, actual_query)
        self.assertNotIn(relevant_notification, actual_query)
