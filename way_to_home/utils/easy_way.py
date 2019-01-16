"""
    This module use for parsing data got in real time from 'Easy Way' source
    in GTFS format.
"""

from google import protobuf  # pylint: disable=no-name-in-module, unused-import
from google.transit import gtfs_realtime_pb2


def compile_file(file_gtfs):
    """ This function compile gtfs file to json file """
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
    """ This function create json file that contain necessary data about certain route """
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
