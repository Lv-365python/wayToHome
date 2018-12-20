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
