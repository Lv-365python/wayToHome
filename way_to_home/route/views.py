"""
Route view module
================

This module that provides base logic for CRUD of route`s model objects.
"""

from django.views import View
from django.http import HttpResponse, JsonResponse

from route.models import Route


class RouteView(View):
    """
    Route view that handles GET, POST, PUT, DELETE requests and provides appropriate
    operations with route model.
    """

    def get(self, request, route_id=None):
        """ Method that handles GET request. """

        route = Route.get_by_id(obj_id=route_id)
        if not route:
            return HttpResponse('database operation is failed, route not found', status=400)

        return JsonResponse(route.to_dict(), status=200)

    def put(self, request, route_id=None):
        """ Method that handles PUT request. """

        route = Route.get_by_id(obj_id=route_id)

        data = request.body

        if not data:
            return HttpResponse('database operation is failed, data not found', status=404)

        if not route:
            return HttpResponse('database operation is failed, route not found', status=404)

        data = {
            'time': data.get('time'),
            'transport_id': data.get('transport_id'),
            'position': data.get('position'),
            'way': data.get('way_id'),
            'start_place': data.get('start_place'),
            'end_place': data.get('end_place'),
        }

        route.update(**data)

        return HttpResponse('database is updated', status=200)

    def post(self, request):
        """ Method that handles POST request. """

        data = request.body

        if not data:
            return HttpResponse('database operation is failed, invalid data', status=400)

        data = {
            'time': data.get('time'),
            'transport_id': data.get('transport_id'),
            'position': data.get('position'),
            'way': data.get('way_id'),
            'start_place': data.get('start_place'),
            'end_place': data.get('end_place'),
        }

        route = Route.create(**data)

        if route:
            route = route.to_dict()
            return JsonResponse(route, status=201)

        return HttpResponse('database operation in failed', status=400)

    def delete(self, route_id=None):
        """ Method that handles DELETE request. """

        route = Route.get_by_id(obj_id=route_id)

        if not route:
            return HttpResponse('database operation is failed, route not found', status=404)

        is_deleted = Route.delete_by_id(route_id)

        if not is_deleted:
            return HttpResponse('database operation is failed', status=400)

        return HttpResponse('route is deleted', status=200)
