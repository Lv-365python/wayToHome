"""
Maps helper Test
========================
This module provides complete testing for all maps helper.
"""
from unittest.mock import patch

from django.test import TestCase

from utils.mapshelper import get_vehicle_time, find_closest_bus_time


class MockRequests:
    def get(self, *args, **kwargs):
        return MockJson()


class MockJson:
    def json(self):
        directions_dict = {'routes': [{'legs': [{'duration': {'value': 123}}]}]}
        return directions_dict


class MapsHelperTestCase(TestCase):
    """Test Case that provides tests for maps helpers"""
    @patch('utils.mapshelper.get_vehicle_time', return_value=123)
    @patch('utils.mapshelper.get_preparing_time', return_value=100)
    def test_find_closest_bus_time_success(self, get_vehicle_time, get_preparing_time):
        """Method that tests the find_closest_bus_time function"""
        test_buses = ['49.870570,24.031429']
        expected_result = 123
        result = find_closest_bus_time(test_buses, '', '')
        self.assertEqual(result, expected_result)

    @patch('utils.mapshelper.get_vehicle_time', return_value=123)
    @patch('utils.mapshelper.get_preparing_time', return_value=200)
    def test_find_closest_bus_time_fail(self, get_vehicle_time, get_preparing_time):
        """Method that tests the find_closest_bus_time function"""
        test_buses = ['49.870570,24.031429']
        result = find_closest_bus_time(test_buses, '', '')
        self.assertIsNone(result)

    @patch('utils.mapshelper.requests.get', MockRequests.get)
    def test_get_vehicle_time(self):
        """Method that tests the get_vehicle_time function"""
        expected_result = 123
        result = get_vehicle_time('', '')
        self.assertEqual(result, expected_result)
