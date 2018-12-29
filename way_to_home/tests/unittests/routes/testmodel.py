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
        user = CustomUser.objects.create(id=1, email='testuser@mail.com', password='testpassword', is_active=True)
        way = Way.objects.create(id=1, user=user)
        start_place = Place.objects.create(id=1, longitude=111.123456, latitude=222.123456)
        end_place = Place.objects.create(id=2, longitude=222.123456, latitude=111.123456)

        Route.objects.create(
            id=100,
            way=way,
            time='01:01:01',
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
