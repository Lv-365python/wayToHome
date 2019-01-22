"""This module provides tests for Route views."""
import datetime
import json
from unittest import mock

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
        user = CustomUser.objects.create(id=100, email='testuser@mail.com', is_active=True)
        user.set_password('testpassword')
        user.save()

        self.client = Client()
        self.client.login(email='testuser@mail.com', password='testpassword')

        way_first = Way.objects.create(id=100, user=user)
        way_second = Way.objects.create(id=101, user=user)

        Notification.objects.create(
            id=100,
            way=way_first,
            start_time=datetime.date(2019, 10, 29),
            end_time=datetime.date(2019, 12, 29),
            week_day=6,
            time=datetime.time(23, 58, 59)
        )

        Notification.objects.create(
            id=101,
            way=way_first,
            start_time=datetime.date(2019, 11, 27),
            end_time=datetime.date(2020, 12, 27),
            week_day=1,
            time=datetime.time(1, 12, 38)
        )

        Notification.objects.create(
            id=102,
            way=way_second,
            start_time=datetime.date(2019, 3, 11),
            end_time=datetime.date(2019, 7, 31),
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
            'start_time': datetime.date(2019, 10, 29),
            'end_time': datetime.date(2019, 12, 29),
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
                'start_time': '2019-11-27',
                'end_time': '2020-12-27',
                'week_day': 1,
                'time': datetime.time(1, 12, 38),
                'way': 100
            },
            {
                'id': 100,
                'start_time': '2019-10-29',
                'end_time': '2019-12-29',
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

    def test_post_success(self):
        """Method that tests the success post request for creating notification."""

        data = {
            'start_time': '2019-10-29',
            'end_time': '2019-12-29',
            'week_day': 6,
            'time': '23:58:59'
        }

        expected_data = {
            'way': 100,
            'start_time': '2019-10-29',
            'end_time': '2019-12-29',
            'week_day': 6,
            'time': '23:58:59'
        }

        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id, 'notification_id': self.notification.id})
        response = self.client.post(url, json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        response_dict = json.loads(response.content)
        response_dict.pop('id')
        self.assertEqual(response.status_code, 201)
        self.assertDictEqual(response_dict, expected_data)

    def test_post_invalid_data(self):
        """Method that tests unsuccessful post request for creating notification with invalid post data."""
        data = {
            'week_day': 'd',
            'time': 'd'
        }
        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id, 'notification_id': self.notification.id})
        response = self.client.post(url, json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_empty_json(self):
        """Method that tests unsuccessful post request with empty JSON data."""

        data = {}
        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id, 'notification_id': self.notification.id})
        response = self.client.post(url, json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_wrong_way_id(self):
        """Provide tests post request for creating notification with another `way_id`."""
        data = {
            'start_time': '2019-10-29',
            'end_time': '2019-12-29',
            'week_day': 6,
            'time': '23:58:59'
        }
        url = reverse('notification', kwargs={'way_id': 908, 'notification_id': self.notification.id})
        response = self.client.post(url, json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_post_non_owner(self):
        """Method that tests for request to update non owner Notification instance."""
        another_user = CustomUser.objects.create(id=1067, email='another_user1@mail.com', is_active=True)
        another_user.set_password('testpassword')
        another_user.save()

        self.client.login(email='another_user1@mail.com', password='testpassword')

        data = {
            'start_time': '2019-10-29',
            'end_time': '2019-12-29',
            'week_day': 6,
            'time': '23:58:59'
        }

        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id, 'notification_id': self.notification.id})
        response = self.client.post(url, json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_db_creating_post(self):
        """Method that tests when notification was not created"""
        data = {
            'start_time': '2019-10-29',
            'end_time': '2019-12-29',
            'week_day': 6,
            'time': '23:58:59'
        }

        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id, 'notification_id': self.notification.id})

        with mock.patch('notification.views.Notification.create') as notification_create:
            notification_create.return_value = False
            response = self.client.post(url, json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')

        self.assertEqual(response.status_code, 400)

    def test_put_success(self):
        """Method that test success put request for the updating Notification"""

        data = {
            'time': '23:58:53'
        }

        url = reverse('notification', kwargs={'way_id': self.notification.way_id, 'notification_id': self.notification.id})
        response = self.client.put(url, json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_put_non_owner(self):
        """Method that tests for request to update non owner Notification instance."""
        another_user = CustomUser.objects.create(id=1067, email='another_user1@mail.com', is_active=True)
        another_user.set_password('testpassword')
        another_user.save()

        self.client.login(email='another_user1@mail.com', password='testpassword')

        data = {
            'week_day': 3
        }

        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id, 'notification_id': self.notification.id})
        response = self.client.put(url, json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_put_wrong_notification_id(self):
        """Method that tests request to update non existent object."""

        data = {
            'time': '23:38:54'
        }

        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id, 'notification_id': 6778})
        response = self.client.put(url, json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_wrong_way_id(self):
        """Provide tests post request for updating notification with another `way_id`."""
        data = {
            'start_time': '2019-10-29',
            'end_time': '2019-12-29',
            'week_day': 6,
            'time': '23:58:59'
        }
        url = reverse('notification', kwargs={'way_id': 543, 'notification_id': self.notification.id})
        response = self.client.put(url, json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_from_another_way(self):
        """Provide tests post request for updating notification with another `way_id`."""
        data = {
            'start_time': '2019-10-29',
            'end_time': '2019-12-29',
            'week_day': 6,
            'time': '23:58:59'
        }
        url = reverse('notification', kwargs={'way_id': 101, 'notification_id': self.notification.id})
        response = self.client.put(url, json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_put_non_id(self):
        """Method that tests request to update object without notification id."""

        data = {
            'time': '23:38:54'
        }

        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id})
        response = self.client.put(url, json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_invalid_data(self):
        """Method that tests unsuccessful put request with invalid data."""

        data = {
            'start_time': '201-10-29'
        }
        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id, 'notification_id': self.notification.id})
        response = self.client.put(url, json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_db_creating_put(self):
        """Method that tests unsuccessful put request when db creating is failed."""
        data = {
            'start_time': '2019-10-29',
            'end_time': '2019-12-29',
            'week_day': 6,
            'time': '23:58:59'
        }
        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id, 'notification_id': self.notification.id})

        with mock.patch('utils.abstract_models.AbstractModel.update') as notification_update:
            notification_update.return_value = False

            response = self.client.put(url, json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_delete_success(self):
        """Method that tests successful delete request"""

        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id, 'notification_id': self.notification.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 200)

    def test_delete_wrong_notification_id(self):
        """Method that tests request to delete non existent object."""

        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id, 'notification_id': 87876})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 400)

    def test_delete_wrong_way_id(self):
        """Method that tests request to delete non existent object."""

        url = reverse('notification',
                      kwargs={'way_id': 38987, 'notification_id': self.notification.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 400)

    def test_delete_another_way_id(self):
        """Provide tests for request to delete Notification instance with another `way_id`."""

        url = reverse('notification',
                      kwargs={'way_id': 101, 'notification_id': self.notification.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 403)

    def test_delete_non_owner(self):
        """Method that tests for request to delete non owner Notification instance."""
        another_user = CustomUser.objects.create(id=134, email='another_user2@mail.com', is_active=True)
        another_user.set_password('qwerty12345')
        another_user.save()

        self.client.login(email='another_user2@mail.com', password='qwerty12345')

        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id, 'notification_id': 87876})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 403)

    def test_delete_non_notification_id(self):
        """Method that tests request to delete object without id."""

        url = reverse('notification', kwargs={'way_id': self.notification.way_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)

    def test_error_db_deleting(self):
        """Method that tests unsuccessful delete request when db deleting is failed."""

        url = reverse('notification',
                      kwargs={'way_id': self.notification.way_id, 'notification_id': self.notification.id})
        with mock.patch('notification.views.Notification.delete_by_id') as notification_delete:
            notification_delete.return_value = False
            response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)
