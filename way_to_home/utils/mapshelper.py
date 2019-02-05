"""This module provides helper functionality to work with google maps data."""

import requests

from django.conf import settings

GOOGLE_DIRECTIONS_JSON_URL = 'https://maps.googleapis.com/maps/api/directions/json'


def find_closest_bus_time(buses_coords, bus_stop_coords):
    """Return arriving time of the closest bus to the stop."""
    vehicles_time = []
    for bus in buses_coords:
        time = get_vehicle_time(bus, bus_stop_coords)
        vehicles_time.append(time)

    closest_bus_time = min(vehicles_time)
    return closest_bus_time


def get_vehicle_time(bus_coords, bus_stop_coords):
    """Return arriving time of the bus to the appropriate bus stop."""
    params = {'origin': bus_coords,
              'destination': bus_stop_coords,
              'key': settings.GOOGLE_API_KEY}

    response = requests.get(GOOGLE_DIRECTIONS_JSON_URL, params=params)
    vehicle = response.json()
    time = vehicle['routes'][0]['legs'][0]['duration']['value']

    return time
