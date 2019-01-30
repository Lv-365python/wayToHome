"""
Place model tests
===============
"""
from decimal import Decimal

from custom_user.models import CustomUser
from django.test import TestCase, Client

from place.models import Place


class PlaceModelTest(TestCase):
    """TestCase for providing Place model testing"""
    def setUp(self):
        """Method that provides preparation before testing Place model features."""
        custom_user = CustomUser.objects.create(id=2, email='mymail@icloud.com', is_active=True)
        custom_user.set_password('qwerty12345')
        custom_user.save()

        self.place = Place.objects.create(
            id=11,
            longitude=49.842601,
            latitude=23.968448,
            address='Широка 34, 79052',
            name='Дім',
            stop_id=None,
            user=custom_user
        )

    def test_get_by_id(self):
        """Provide tests for `get_by_id` method of certain Place instance."""
        expected_place = Place.objects.get(id=self.place.id)
        actual_place = Place.get_by_id(obj_id=self.place.id)
        self.assertEqual(expected_place, actual_place)

        unexisting_place = Place.get_by_id(obj_id=111)
        self.assertIsNone(unexisting_place)
        self.assertRaises(Place.DoesNotExist, Place.objects.get, id=111)

    def test_delete_by_id(self):
        """Provide tests for `delete_by_id` method of certain Place instance."""
        is_deleted = Place.delete_by_id(obj_id=self.place.id)
        self.assertTrue(is_deleted)
        self.assertRaises(Place.DoesNotExist, Place.objects.get, id=self.place.id)

        is_deleted = Place.delete_by_id(obj_id=111)
        self.assertFalse(is_deleted)

    def test_to_dict(self):
        """Provide tests for `to_dict` method of certain Place instance."""
        place = Place.get_by_id(obj_id=self.place.id)

        expected_dict = {
            'id': 11,
            'longitude': Decimal('49.842601'),
            'latitude': Decimal('23.968448'),
            'name': 'Дім',
            'address': 'Широка 34, 79052',
            'stop_id': None,
            'user_id': 2
        }
        actual_dict = place.to_dict()
        self.assertDictEqual(expected_dict, actual_dict)

    def test_str(self):
        """Provide tests for `__str__` method of certain Place instance."""
        place = Place.get_by_id(obj_id=self.place.id)

        expected_string = '49.842601, 23.968448'
        actual_string = place.__str__()

        self.assertEqual(expected_string, actual_string)

    def test_create(self):
        """Provide tests for `create` method of Place model."""
        user = CustomUser.objects.get(id=2)
        place = Place.create(
            longitude=49.842601,
            latitude=23.968448,
            name='Дім',
            address='Широка 34, 79052',
            user=user
        )

        self.assertIsInstance(place, Place)
        self.assertIsNotNone(Place.objects.get(id=self.place.id))

        place = Place.create(longitude=Decimal(), latitude=Decimal(), name='', user=CustomUser())
        self.assertIsNone(place)

    def test_update(self):
        """Provide tests for `update` method of certain Place instance."""
        update_data = {
            'name': 'Робота',
            'longitude': Decimal('23.968412'),
            'latitude': Decimal('48.968412'),
            'address': 'Степана Бандери 12, 79052'
        }
        is_updated = self.place.update(**update_data)
        self.assertTrue(is_updated)

        place = Place.objects.get(id=self.place.id)
        for key, value in update_data.items():
            self.assertEqual(place.__dict__[key], value)

        new_stop_id = -1
        is_updated = self.place.update(stop_id=new_stop_id)
        self.assertFalse(is_updated)
        place = Place.objects.get(id=self.place.id)
        self.assertNotEqual(place.latitude, new_stop_id)
