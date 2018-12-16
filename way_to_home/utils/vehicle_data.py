"""
    This module use for parsing data got in real time from 'Easy Way' source
    in GTFS format.
"""

import google.protobuf
from google.transit import gtfs_realtime_pb2
import requests


FEED = gtfs_realtime_pb2.FeedMessage()
RESPONSE = requests.get('http://track.ua-gis.com/gtfs/lviv/vehicle_position')
FEED.ParseFromString(RESPONSE.content)


def get_vehicle_data(vehicle_id):
    """
        This function takes certain vehicle id as parameter and
        returns appropriate data about it's location, speed etc.
    """
    vehicle_data_json = {}
    for entity in FEED.entity:
        if entity.vehicle.vehicle.id == vehicle_id:
            vehicle_data_json['route_id'] = entity.vehicle.trip.route_id
            vehicle_data_json['lat'] = entity.vehicle.position.latitude
            vehicle_data_json['lon'] = entity.vehicle.position.longitude
            vehicle_data_json['speed'] = entity.vehicle.position.speed
    return vehicle_data_json


if __name__ == '__main__':
    print(get_vehicle_data('2593'))
