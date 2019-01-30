"""This module provides functionality to work with data from EasyWay."""

from collections import defaultdict

from google import protobuf  # pylint: disable=no-name-in-module, unused-import
from google.transit import gtfs_realtime_pb2

from .file_handlers import parse_csv_file


def compile_file(file_gtfs):
    """This function compile GTFS file to json file."""
    feed = gtfs_realtime_pb2.FeedMessage()

    try:
        with open(file_gtfs, 'rb') as file:
            content = file.read()
    except (FileNotFoundError, PermissionError):
        return None

    feed.ParseFromString(content)
    gtfs_data = parse_vehicle_data(feed.entity)  # pylint: disable=no-member

    return gtfs_data


def parse_vehicle_data(feed_entity):
    """This function create dictionary that contain necessary data about certain route."""
    vehicle_data = {}
    for entity in feed_entity:
        route_id = entity.vehicle.trip.route_id  # identifier of the certain route
        if not vehicle_data.get(route_id):
            vehicle_data[route_id] = []

        vehicle_data[route_id].append({
            'trip_id': entity.vehicle.trip.trip_id,  # identifier of trip
            'lat': entity.vehicle.position.latitude,  # latitude in WGS-84 coordinate system
            'lon': entity.vehicle.position.longitude,  # longitude in WGS-84 coordinate system
            'vehicle_id': entity.vehicle.vehicle.id  # identifier of vehicle
        })

    return vehicle_data


def parse_trips_data(file_path='./trips.txt'):
    """
    Return data about trips as dictionary where key
    is id of route and value is list of trips ids.
    """
    trips_content = parse_csv_file(file_path, ['route_id', 'trip_id'])

    trips = defaultdict(list)
    for trip in trips_content:
        key = trip.get('route_id')
        value = trip.get('trip_id')
        trips[key].append(value)

    return trips


def parse_routes_data(file_path='./routes.txt'):
    """
    Return data about routes as dictionary where key is id
    of route and value is short name of appropriate route.
    """
    routes_content = parse_csv_file(file_path, ['route_id', 'route_short_name'])

    routes = {}
    for route in routes_content:
        key = route.get('route_id')
        value = route.get('route_short_name')
        routes[key] = value

    return routes


def parse_stops_data(file_path='./stops.txt'):
    """
    Return data about stops as dictionary where key is id of stop and
    value is tuple with latitude and longitude of appropriate stop.
    """
    stops_content = parse_csv_file(file_path, ['stop_id', 'stop_lat', 'stop_lon'])

    stops = {}
    for stop in stops_content:
        key = stop.get('stop_id')
        latitude = stop.get('stop_lat')
        longitude = stop.get('stop_lon')
        stops[key] = (latitude, longitude)

    return stops
