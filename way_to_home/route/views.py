"""
Route view module
================

This module that provides base logic for CRUD of route`s model objects.
"""

from django.http import JsonResponse
from django.views import View
from route.models import Route


class RouteView(View):
    """
    Route view that handles GET, POST, PUT, DELETE requests and provides appropriate
    operations with route model.
    """

    def get(self, route_id=None):
        """ Method that handles GET request. """

        if route_id:
            route = Route.get_by_id(obj_id=route_id)
            if not route:
                return 404

        return JsonResponse(route.to_dict(), status=200)

    def post(self):
        """ Method that handles POST request. """

    def put(self):
        """ Method that handles PUT request. """

    def delete(self):
        """ Method that handles DELETE request. """
