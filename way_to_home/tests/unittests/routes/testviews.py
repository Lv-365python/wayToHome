"""This module provides tests for Route views."""
import json

from django.test import TestCase, Client
from django.urls import reverse

from custom_user.models import CustomUser
from place.models import Place
from route.models import Route
from way.models import Way


class RouteViewsTestCase(TestCase):
    """TestCase for providing Route views testing."""

    def setUp(self):
        """Method that provides preparation before testing Route views."""
        user = CustomUser(id=100, email='testuser@mail.com', is_active=True)
        user.set_password('testpassword')
        user.save()

        way_first = Way.objects.create(id=100, user=user)
        way_second = Way.objects.create(id=101, user=user)
        start_place = Place.objects.create(id=100, longitude=111.123456, latitude=222.123456)
        end_place = Place.objects.create(id=200, longitude=222.123456, latitude=111.123456)

        Route.objects.create(
            id=100,
            way=way_first,
            time='23:58:59',
            position=0,
            start_place=start_place,
            end_place=end_place
        )

        Route.objects.create(
            id=101,
            way=way_first,
            time='01:02:03',
            position=1,
            start_place=start_place,
            end_place=end_place
        )

        Route.objects.create(
            id=102,
            way=way_second,
            time='11:22:33',
            position=1,
            start_place=start_place,
            end_place=end_place
        )

        self.route = Route.objects.get(id=100)
        self.client = Client()
        self.client.login(email='testuser@mail.com', password='testpassword')

    def test_get_one(self):
        """Provide tests for request to retrieve certain Route instance."""
        expected_response = {
            "id": 100, "time": "23:58:59", "transport_id": None, "position": 0,
            "way": 100,  "end_place": 200, "start_place": 100
        }
        url = reverse('route', kwargs={'way_id': self.route.way_id, 'route_id': self.route.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(json.dumps(expected_response), json.loads(response.content))

    def test_get_all(self):
        """Provide tests for request to retrieve all way`s routes"""
        expected_response = [
            {
                'id': 100, 'time': '23:58:59', 'transport_id': None, 'position': 0,
                'way': 100,  'start_place': 100, 'end_place': 200
             },
            {
                'id': 101, 'time': '01:02:03', 'transport_id': None, 'position': 1,
                'way': 100, 'start_place': 100, 'end_place': 200
            }
        ]
        url = reverse('route', kwargs={'way_id': self.route.way_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(json.dumps(expected_response), json.loads(response.content))

    def test_get_not_found(self):
        """Provide tests for request to retrieve non existent objects."""
        url = reverse('route', kwargs={'way_id': 999, 'route_id': 100})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        url = reverse('route', kwargs={'way_id': 100, 'route_id': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_get_non_owner(self):
        """Provide tests for request to retrieve non owner Route instance."""
        another_user = CustomUser(id=101, email='another_user@mail.com', is_active=True)
        another_user.set_password('testpassword')
        another_user.save()
        self.client.login(email='another_user@mail.com', password='testpassword')

        url = reverse('route', kwargs={'way_id': self.route.way_id, 'route_id': self.route.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_get_from_another_way(self):
        """Provide tests for request to retrieve Route instance with another `way_id`."""
        url = reverse('route', kwargs={'way_id': 101, 'route_id': self.route.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
