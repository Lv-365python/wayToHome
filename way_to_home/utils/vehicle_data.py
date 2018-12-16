from google.protobuf import json_format
from google.transit import gtfs_realtime_pb2
import requests


feed = gtfs_realtime_pb2.FeedMessage()
response = requests.get('http://track.ua-gis.com/gtfs/lviv/vehicle_position')
feed.ParseFromString(response.content)


def get_vehicle_data(vehicle_id):
    """
    This function takes certain vehicle id as parameter and
    returns appropriate data about it's location, speed etc.
    """
    vehicle_data_json = {}
    for entity in feed.entity:
        if entity.vehicle.vehicle.id == vehicle_id:
            vehicle_data_json['route_id'] = entity.vehicle.trip.route_id
            vehicle_data_json['lat'] = entity.vehicle.position.latitude
            vehicle_data_json['lon'] = entity.vehicle.position.longitude
            vehicle_data_json['speed'] = entity.vehicle.position.speed
    return vehicle_data_json


if __name__ == '__main__':
    print(get_vehicle_data('2593'))
