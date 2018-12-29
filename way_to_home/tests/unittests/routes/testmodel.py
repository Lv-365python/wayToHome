"""This module provides tests for Route model."""

import datetime

from django.test import TestCase

from custom_user.models import CustomUser
from place.models import Place
from route.models import Route
from way.models import Way


class RouteModelTestCase(TestCase):
    """TestCase for providing Route model testing."""

    def setUp(self):
        """Method that provides preparation before testing Route model's features."""
        user = CustomUser.objects.create(id=100, email='testuser@mail.com', password='testpassword', is_active=True)
        way = Way.objects.create(id=100, user=user)
        start_place = Place.objects.create(id=100, longitude=111.123456, latitude=222.123456)
        end_place = Place.objects.create(id=200, longitude=222.123456, latitude=111.123456)

        Route.objects.create(
            id=100,
            way=way,
            time='23:58:59',
            position=0,
            start_place=start_place,
            end_place=end_place
        )
        self.route = Route.objects.get(id=100)

    def test_get_by_id(self):
        """Provide tests for `get_by_id` method of certain Route instance."""
        expected_route = Route.objects.get(id=self.route.id)
        actual_route = Route.get_by_id(obj_id=self.route.id)
        self.assertEqual(expected_route, actual_route)

        unexisting_route = Route.get_by_id(obj_id=999)
        self.assertIsNone(unexisting_route)
        self.assertRaises(Route.DoesNotExist, Route.objects.get, id=999)

    def test_delete_by_id(self):
        """Provide tests for `delete_by_id` method of certain Route instance."""
        is_deleted = Route.delete_by_id(obj_id=self.route.id)
        self.assertTrue(is_deleted)
        self.assertRaises(Route.DoesNotExist, Route.objects.get, id=self.route.id)

        is_deleted = Route.delete_by_id(obj_id=999)
        self.assertFalse(is_deleted)

    def test_to_dict(self):
        """Provide tests for `to_dict` method of certain Route instance."""
        route = Route.objects.get(id=self.route.id)

        expected_dict = {
            'id': 100,
            'time':  datetime.time(23, 58, 59),
            'transport_id': None,
            'position': 0,
            'way': 100,
            'start_place': 100,
            'end_place': 200,
        }
        actual_dict = route.to_dict()
        self.assertDictEqual(expected_dict, actual_dict)

    def test_str(self):
        """Provide tests for `__str__` method of certain Route instance."""
        route = Route.objects.get(id=self.route.id)

        expected_string = 'route from: 100 to 200'
        actual_string = route.__str__()

        self.assertEqual(expected_string, actual_string)

    def test_create(self):
        """Provide tests for `create` method of Route model."""
        way = Way.objects.get(id=100)
        start_place = Place.objects.get(id=100)
        end_place = Place.objects.get(id=200)

        route = Route.create(way=way, time='01:02:03', position=1, start_place=start_place, end_place=end_place)
        self.assertIsInstance(route, Route)
        self.assertIsNotNone(Route.objects.get(id=route.id))

        route = Route.create(way=Way(), time='', position=-1, start_place=Place(), end_place=Place())
        self.assertIsNone(route)

    def test_update(self):
        """Provide tests for `update` method of certain Route instance."""
        new_time = datetime.time(1, 2, 3)
        new_position = 99
        is_updated = self.route.update(time=new_time, position=new_position)
        self.assertTrue(is_updated)

        route = Route.objects.get(id=self.route.id)
        self.assertEqual(route.position, new_position)
        self.assertEqual(route.time, new_time)

        new_position = -1
        is_updated = self.route.update(position=new_position)
        self.assertFalse(is_updated)
        route = Route.objects.get(id=self.route.id)
        self.assertNotEqual(route.position, new_position)
