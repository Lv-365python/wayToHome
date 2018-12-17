"""
    This module use for parsing data got in real time from 'Easy Way' source
    in GTFS format.
"""
import requests
from google import protobuf
from google.transit import gtfs_realtime_pb2


def get_vehicle_data(route_id):
    """
        This function takes certain route id as parameter and
        returns appropriate data about it's location.
        Argument:
            route_id(str): identifier of the certain route.
        Returns:
            vehicle_data_json(dict): the dictionary contains data about
            a certain vehicle that belongs to the inputted route.
            Keys:
                "trip_id": identifier of trip;
                "lat": latitude in WGS-84 coordinate system;
                "lon": longitude in WGS-84 coordinate system;
                "vehicle_id": identifier of vehicle.
    """
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get('http://track.ua-gis.com/gtfs/lviv/vehicle_position')
    feed.ParseFromString(response.content)
    vehicle_data = {}
    for entity in feed.entity:
        if entity.vehicle.trip.route_id == route_id:
            vehicle_data["trip_id"] = entity.vehicle.trip.trip_id
            vehicle_data["lat"] = entity.vehicle.position.latitude
            vehicle_data["lon"] = entity.vehicle.position.longitude
            vehicle_data["vehicle_id"] = entity.vehicle.vehicle.id
    return vehicle_data
