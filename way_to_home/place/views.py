"""This module that provides base logic for CRUD of place`s model objects."""

from django.http import HttpResponse, JsonResponse
from django.views import View

from utils.validators import place_data_validator
from .models import Place


class PlaceView(View):
    """Class that handle HTTP requests for place model."""

    def post(self, request, place_id=None):
        """Handle the request to create a new place object."""
        data = request.body
        if not data:
            return HttpResponse('empty json received', status=400)

        data = {
            'longitude': data.get('longitude'),
            'latitude': data.get('latitude'),
            'address': data.get('address'),
            'name': data.get('name'),
            'stop_id': data.get('stop_id')
        }

        if not place_data_validator(data):
            return HttpResponse('invalid data', status=400)

        place = Place.create(user=request.user, **data)
        if not place:
            return HttpResponse('database operation is failed', status=400)

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
            return HttpResponse('object not found', status=400)

        if place.user and place.user != user:
            return HttpResponse('access denied for non-owner users', status=403)

        place = place.to_dict()
        return JsonResponse(place, status=200)

    def put(self, request, place_id=None):  # pylint: disable=R0201, R0911
        """Handle the request to update an existing place object with appropriate id."""
        user = request.user

        if not place_id:
            return HttpResponse('object id is not received', status=400)

        data = request.body
        if not data:
            return HttpResponse('empty json received', status=400)

        place = Place.get_by_id(place_id)

        if not place:
            return HttpResponse('object not found', status=400)

        if place.user and place.user != user:
            return HttpResponse('access denied for non-owner users', status=403)

        data = {
            'longitude': data.get('longitude'),
            'latitude': data.get('latitude'),
            'address': data.get('address'),
            'name': data.get('name'),
            'stop_id': data.get('stop_id')
        }

        if not place_data_validator(data, update=True):
            return HttpResponse('invalid data', status=400)

        is_updated = place.update(**data)
        if not is_updated:
            return HttpResponse('database operation is failed', status=400)

        return HttpResponse('object was successfully updated', status=200)

    def delete(self, request, place_id=None):  # pylint: disable=R0201
        """Handle the request to delete place object with appropriate id."""
        user = request.user
        if not place_id:
            return HttpResponse('object id is not received', status=400)

        place = Place.get_by_id(place_id)

        if not place:
            return HttpResponse('object not found', status=400)

        if place.user and place.user != user:
            return HttpResponse('access denied for non-owner user', status=403)

        is_deleted = Place.delete_by_id(place_id)
        if not is_deleted:
            return HttpResponse('database operation is failed', status=400)

        return HttpResponse('object was successfully deleted', status=204)
