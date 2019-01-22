"""
Route view module
================

This module that provides base logic for CRUD of route`s model objects.
"""

from django.views import View
from django.http import JsonResponse

from route.models import Route
from way.models import Way
from utils.validators import route_data_validator
from utils.responsehelper import (RESPONSE_400_OBJECT_NOT_FOUND,
                                  RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_200_UPDATED,
                                  RESPONSE_200_DELETED)


class RouteView(View):
    """
    Route view that handles GET, POST, PUT, DELETE requests and provides appropriate
    operations with route model.
    """

    http_method_names = ['get']

    def get(self, request, way_id, route_id=None):
        """ Method that handles GET request. """
        user = request.user
        way = Way.get_by_id(obj_id=way_id)

        if not way:
            return RESPONSE_400_OBJECT_NOT_FOUND

        if not user == way.user:
            return RESPONSE_403_ACCESS_DENIED

        if not route_id:
            data = [route.to_dict() for route in way.routes.all().order_by('position')]
            return JsonResponse(data, status=200, safe=False)

        route = Route.get_by_id(obj_id=route_id)
        if not route:
            return RESPONSE_400_OBJECT_NOT_FOUND

        if not way == route.way:
            return RESPONSE_403_ACCESS_DENIED

        return JsonResponse(route.to_dict(), status=200)
