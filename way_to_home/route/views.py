"""
Route view module
================

This module that provides base logic for CRUD of route`s model objects.
"""

from django.views import View
from django.http import HttpResponse, JsonResponse

from route.models import Route
from way.models import Way
from utils.validators import route_data_validator


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
            return HttpResponse('failed, way not found', status=400)

        if not user == way.user:
            return HttpResponse('Permission denied', status=403)

        if not route_id:
            data = [route.to_dict() for route in way.routes.all().order_by('position')]
            return JsonResponse(data, status=200, safe=False)

        route = Route.get_by_id(obj_id=route_id)
        if not route:
            return HttpResponse('Route not found', status=400)

        if not way == route.way:
            return HttpResponse('Permission denied', status=403)

        return JsonResponse(route.to_dict(), status=200)

    def put(self, request, way_id, route_id=None):  # pylint: disable=R0201, R0911
        """ Method that handles PUT request. """
        user = request.user
        data = request.body
        way = Way.get_by_id(obj_id=way_id)

        if not (way or route_id):
            return HttpResponse('failed, objects not found', status=400)

        if not user == way.user:
            return HttpResponse('Permission denied', status=403)

        route = Route.get_by_id(obj_id=route_id)
        if not route:
            return HttpResponse('Route not found', status=400)

        if not way == route.way:
            return HttpResponse('Permission denied', status=403)

        data = {
            'time': data.get('time'),
            'transport_id': data.get('transport_id'),
            'position': data.get('position'),
            'start_place': data.get('start_place'),
            'end_place': data.get('end_place'),
        }

        if not route_data_validator(data, update=True):
            return HttpResponse('Invalid data', status=400)

        is_updated = route.update(**data)
        if not is_updated:
            return HttpResponse('database was not updated', status=400)

        return HttpResponse('database is updated', status=200)

    def post(self, request, way_id, route_id=None):
        """ Method that handles POST request. """
        user = request.user
        data = request.data
        way = Way.get_by_id(obj_id=way_id)

        if not way:
            return HttpResponse('failed, way not found', status=400)

        if not user == way.user:
            return HttpResponse('Permission denied', status=403)

        data = {
            'time': data.get('time'),
            'transport_id': data.get('transport_id'),
            'position': data.get('position'),
            'start_place': data.get('start_place'),
            'end_place': data.get('end_place'),
            'way': way,
        }

        if not route_data_validator(data):
            return HttpResponse('Invalid data', status=400)

        route = Route.create(**data)
        if not route:
            return HttpResponse('database operation in failed', status=400)

        return JsonResponse(route.to_dict(), status=201)

    def delete(self, request, way_id, route_id=None):  # pylint: disable=R0201
        """ Method that handles DELETE request. """
        user = request.user
        way = Way.get_by_id(obj_id=way_id)

        if not (way or route_id):
            return HttpResponse('failed, objects not found', status=400)

        if not user == way.user:
            return HttpResponse('Permission denied', status=403)

        route = Route.get_by_id(obj_id=route_id)
        if not route:
            return HttpResponse('Route not found', status=400)

        if not way == route.way:
            return HttpResponse('Permission denied', status=403)

        is_deleted = Way.delete_by_id(obj_id=way_id)
        if not is_deleted:
            return HttpResponse('database operation is failed', status=400)

        return HttpResponse('route is deleted', status=200)
