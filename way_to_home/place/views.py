"""This module that provides base logic for CRUD of place`s model objects."""

from django.http import JsonResponse
from django.views import View

from utils.validators import place_data_validator
from utils.responsehelper import (RESPONSE_200_UPDATED,
                                  RESPONSE_200_DELETED,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_400_OBJECT_NOT_RECEIVED,
                                  RESPONSE_400_EMPTY_JSON,
                                  RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_404_OBJECT_NOT_FOUND,
                                  )
from .models import Place


class PlaceView(View):
    """Class that handle HTTP requests for place model."""

    def post(self, request, place_id=None):
        """Handle the request to create a new place object."""
        data = request.body
        if not data:
            return RESPONSE_400_EMPTY_JSON

        data = {
            'longitude': data.get('longitude'),
            'latitude': data.get('latitude'),
            'address': data.get('address'),
            'name': data.get('name'),
            'stop_id': data.get('stop_id')
        }

        if not place_data_validator(data):
            return RESPONSE_400_INVALID_DATA

        place = Place.create(user=request.user, **data)
        if not place:
            return RESPONSE_400_DB_OPERATION_FAILED

        place = place.to_dict()
        return JsonResponse(place, status=201)

    def get(self, request, place_id=None):
        """Handle the request to retrieve a place object or user`s places."""
        user = request.user

        if not place_id:
            places = user.places.all()
            data = [place.to_dict() for place in places]

            return JsonResponse(data, status=200, safe=False)

        place = Place.get_by_id(place_id)
        if not place:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if place.user and place.user != user:
            return RESPONSE_403_ACCESS_DENIED

        place = place.to_dict()
        return JsonResponse(place, status=200)

    def put(self, request, place_id=None):  # pylint: disable=R0201, R0911
        """Handle the request to update an existing place object with appropriate id."""
        user = request.user
        data = request.body

        if not data:
            return RESPONSE_400_EMPTY_JSON

        if not place_id:
            return RESPONSE_400_OBJECT_NOT_RECEIVED

        place = Place.get_by_id(place_id)
        if not place:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if place.user and place.user != user:
            return RESPONSE_403_ACCESS_DENIED

        data = {
            'longitude': data.get('longitude'),
            'latitude': data.get('latitude'),
            'address': data.get('address'),
            'name': data.get('name'),
            'stop_id': data.get('stop_id')
        }

        if not place_data_validator(data, update=True):
            return RESPONSE_400_INVALID_DATA

        is_updated = place.update(**data)
        if not is_updated:
            return RESPONSE_400_DB_OPERATION_FAILED

        return RESPONSE_200_UPDATED

    def delete(self, request, place_id=None):  # pylint: disable=R0201
        """Handle the request to delete place object with appropriate id."""
        user = request.user
        if not place_id:
            return RESPONSE_400_OBJECT_NOT_RECEIVED

        place = Place.get_by_id(place_id)

        if not place:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if place.user and place.user != user:
            return RESPONSE_403_ACCESS_DENIED

        is_deleted = Place.delete_by_id(place_id)
        if not is_deleted:
            return RESPONSE_400_DB_OPERATION_FAILED

        return RESPONSE_200_DELETED
