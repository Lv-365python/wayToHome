"""This module that provides base logic for CRUD of place`s model objects."""

from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import Place


class PlaceView(View):
    """Class that handle HTTP requests for place model."""

    def post(self, request, obj_id=None):
        """Handle the request for create a new place object."""
        data = request.body
        if not data:
            return HttpResponse('empty json received', status=400)

        # if not place_data_validator(data):
        #     return HttpResponse('invalid data', status=400)

        place = Place.create(user=request.user, **data)
        if not place:
            return HttpResponse('database operation is failed', status=400)

        place = place.to_dict()
        return JsonResponse(place, status=201)

    def get(self, request, obj_id=None):
        """Handle the request for retrieve a place object or user`s places."""
        user = request.user

        if not obj_id:
            places = user.places.all()
            data = [place.to_dict() for place in places]

            return JsonResponse(data, status=200, safe=False)

        place = Place.get_by_id(obj_id)

        if not place:
            return HttpResponse('object not found', status=404)

        if place.user_id and place.user_id != user.id:
            return HttpResponse('access denied for non-owner users', status=403)

        place = place.to_dict()
        return JsonResponse(place, status=200)
