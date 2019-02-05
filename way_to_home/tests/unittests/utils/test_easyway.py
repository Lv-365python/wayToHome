"""This module provides tests for Easy Way helpers functions."""

from google.transit import gtfs_realtime_pb2
from collections import defaultdict

from django.test import TestCase
from unittest.mock import patch

from utils.easy_way import (compile_file,
                            parse_trips_data,
                            parse_routes_data,
                            parse_stops_data,
                            _parse_vehicle_data,
                            prettify_gtfs)


class EasyWayTestCase(TestCase):
    """TestCase for providing Easy Way functions testing."""

    def setUp(self):
        """Provides preparation before testing Easy Way helpers functions."""
        self.feed = gtfs_realtime_pb2.FeedMessage()
        self.path_to_gtfs_file = 'tests/unittests/utils/test_vehicle_position'

    def test_compile_file_success(self):
        """Provide tests for `compile_file` function in case of success."""
        with open(self.path_to_gtfs_file, 'rb') as file:
            content = file.read()

        self.feed.ParseFromString(content)
        expected_gtfs_data = _parse_vehicle_data(self.feed.entity)

        actual_gtfs_data = compile_file(self.path_to_gtfs_file)
        self.assertEqual(expected_gtfs_data, actual_gtfs_data)

    def test_compile_file_open_error(self):
        """Provide tests for `compile_file` function in case of open operations is failed."""
        with patch('builtins.open') as open_file:
            open_file.side_effect = FileNotFoundError()
            result = compile_file(self.path_to_gtfs_file)
            self.assertIsNone(result)

            open_file.side_effect = PermissionError()
            result = compile_file(self.path_to_gtfs_file)
            self.assertIsNone(result)

    def test_parse_vehicle_data(self):
        """Provide tests for `parse_vehicle_data` function in case of success."""
        with open(self.path_to_gtfs_file, 'rb') as file:
            content = file.read()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(content)

        expected_vehicle_data = {}
        for entity in feed.entity:
            route_id = entity.vehicle.trip.route_id
            if not expected_vehicle_data.get(route_id):
                expected_vehicle_data[route_id] = []

            expected_vehicle_data[route_id].append({
                'trip_id': entity.vehicle.trip.trip_id,
                'lat': entity.vehicle.position.latitude,
                'lon': entity.vehicle.position.longitude,
                'vehicle_id': entity.vehicle.vehicle.id
            })

        actual_vehicle_data = _parse_vehicle_data(feed.entity)
        self.assertDictEqual(expected_vehicle_data, actual_vehicle_data)

    @patch('utils.easy_way.parse_csv_file')
    def test_parse_trips_data(self, parse_csv):
        """Provide tests for `parse_trips_data` function in case of success."""
        parse_csv_file_data = [
            {'route_id': '129', 'trip_id': '8446_3_1'},
            {'route_id': '129', 'trip_id': '8446_4_0'},
            {'route_id': '129', 'trip_id': '8446_4_1'},
        ]
        parse_csv.return_value = parse_csv_file_data

        expected_trips = defaultdict(list)
        for trip in parse_csv_file_data:
            key = trip.get('route_id')
            value = trip.get('trip_id')
            expected_trips[key].append(value)

        actual_trips = parse_trips_data('path/to/trips/file')
        self.assertDictEqual(expected_trips, actual_trips)

    @patch('utils.easy_way.parse_csv_file')
    def test_parse_routes_data(self, parse_csv):
        """Provide tests for `parse_routes_data` function if case of success."""
        parse_csv_file_data = [
            {'route_id': '88', 'route_short_name': 'А48'},
            {'route_id': '90', 'route_short_name': 'А01'},
            {'route_id': '91', 'route_short_name': 'Н-А01'},
        ]
        parse_csv.return_value = parse_csv_file_data

        expected_routes = {}
        for route in parse_csv_file_data:
            key = route.get('route_id')
            value = route.get('route_short_name')
            expected_routes[key] = value

        actual_routes = parse_routes_data('path/to/routes/file')
        self.assertDictEqual(expected_routes, actual_routes)

    @patch('utils.easy_way.parse_csv_file')
    def test_parse_stops_data(self, parse_csv):
        """Provide tests for `parse_stops_data` function if case of success."""
        parse_csv_file_data = [
            {'stop_id': '5179', 'stop_lat': '49.782854', 'stop_lon': '24.096483'},
            {'stop_id': '5181', 'stop_lat': '49.818161', 'stop_lon': '24.057797'},
            {'stop_id': '5182', 'stop_lat': '49.818116', 'stop_lon': '24.057961'},
        ]
        parse_csv.return_value = parse_csv_file_data

        expected_stops = {}
        for stop in parse_csv_file_data:
            key = stop.get('stop_id')
            latitude = stop.get('stop_lat')
            longitude = stop.get('stop_lon')
            expected_stops[key] = (latitude, longitude)

        actual_stops = parse_stops_data('path/to/stops/file')
        self.assertDictEqual(expected_stops, actual_stops)

    def test_prettify_gtfs(self):
        """Provide tests for `prettify_gtfs` function if case of success."""
        gtfs_data = [{
            'trip_id': '8274_11_0',
            'lat': 49.80548858642578,
            'lon': 24.121530532836914,
            'vehicle_id': '2541'
        }]

        expected_prettified_data = []
        for vehicle in gtfs_data:
            expected_prettified_data.append(f'{vehicle["lat"]},{vehicle["lon"]}')

        actual_prettified_data = prettify_gtfs(gtfs_data)
        self.assertEqual(expected_prettified_data, actual_prettified_data)
