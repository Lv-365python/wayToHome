"""This module provides tests for Route views."""
import datetime
import json

import pytz
from django.core.serializers.json import DjangoJSONEncoder
from django.test import TestCase, Client
from django.urls import reverse

from custom_user.models import CustomUser
from notification.models import Notification
from way.models import Way


class NotificationViewsTestCase(TestCase):
    """TestCase for providing Notification views testing."""

    def setUp(self):
        """Method that provides preparation before testing Notification views."""
        user = CustomUser(id=100, email='testuser@mail.com', is_active=True)
        user.set_password('testpassword')
        user.save()

        way_first = Way.objects.create(id=100, user=user)
        way_second = Way.objects.create(id=101, user=user)

        Notification.objects.create(
            id=100,
            way=way_first,
            start_time=pytz.utc.localize(datetime.datetime.strptime('2019-10-29', '%Y-%m-%d')),
            end_time=pytz.utc.localize(datetime.datetime.strptime('2019-12-29', '%Y-%m-%d')),
            week_day=6,
            time=datetime.time(23, 58, 59)
        )

        Notification.objects.create(
            id=101,
            way=way_first,
            start_time=pytz.utc.localize(datetime.datetime.strptime('2019-11-27', '%Y-%m-%d')),
            end_time=pytz.utc.localize(datetime.datetime.strptime('2020-12-27', '%Y-%m-%d')),
            week_day=1,
            time=datetime.time(1, 12, 38)
        )

        Notification.objects.create(
            id=102,
            way=way_second,
            start_time=pytz.utc.localize(datetime.datetime.strptime('2019-03-11', '%Y-%m-%d')),
            end_time=pytz.utc.localize(datetime.datetime.strptime('2019-07-31', '%Y-%m-%d')),
            week_day=2,
            time=datetime.time(11, 28, 25)
        )

        self.notification = Notification.objects.get(id=100)
        self.client = Client()
        self.client.login(email='testuser@mail.com', password='testpassword')

    def test_get_one(self):
        """Provide tests for request to retrieve certain Notification instance."""
        expected_response = {
            'id': 100,
            'start_time': pytz.utc.localize(datetime.datetime.strptime('2019-10-29', '%Y-%m-%d')),
            'end_time': pytz.utc.localize(datetime.datetime.strptime('2019-12-29', '%Y-%m-%d')),
            'week_day': 6,
            'time': datetime.time(23, 58, 59),
            'way': 100
        }
        url = reverse('notification', kwargs={'way_id': self.notification.way_id, 'notification_id': self.notification.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            json.dumps(expected_response, cls=DjangoJSONEncoder, sort_keys=True),
            json.loads(response.content)
        )

    def test_get_all(self):
        """Provide tests for request to retrieve all way`s Notification"""
        expected_response = [
            {
                'id': 101,
                'start_time': pytz.utc.localize(datetime.datetime.strptime('2019-11-27', '%Y-%m-%d')),
                'end_time': pytz.utc.localize(datetime.datetime.strptime('2020-12-27', '%Y-%m-%d')),
                'week_day': 1,
                'time': datetime.time(1, 12, 38),
                'way': 100
            },
            {
                'id': 100,
                'start_time': pytz.utc.localize(datetime.datetime.strptime('2019-10-29', '%Y-%m-%d')),
                'end_time': pytz.utc.localize(datetime.datetime.strptime('2019-12-29', '%Y-%m-%d')),
                'week_day': 6,
                'time': datetime.time(23, 58, 59),
                'way': 100
             }
        ]
        url = reverse('notification', kwargs={'way_id': self.notification.way_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            json.dumps(expected_response, cls=DjangoJSONEncoder)
        )

    def test_get_not_found(self):
        """Provide tests for request to retrieve non existent objects."""
        url = reverse('notification', kwargs={'way_id': 999, 'notification_id': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

        url = reverse('notification', kwargs={'way_id': 100, 'notification_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_get_non_owner(self):
        """Provide tests for request to retrieve non owner Notification instance."""
        another_user = CustomUser(id=101, email='another_user@mail.com', is_active=True)
        another_user.set_password('testpassword')
        another_user.save()
        self.client.login(email='another_user@mail.com', password='testpassword')

        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id, 'notification_id': self.notification.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_get_from_another_way(self):
        """Provide tests for request to retrieve Notification instance with another `way_id`."""
        url = reverse('notification', kwargs={'way_id': 101, 'notification_id': self.notification.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

