"""This module that provides base logic for CRUD of way`s model objects."""

from django.views.generic import View
from django.http import JsonResponse
from django.db import transaction
import isodate
from way.models import Way
from place.models import Place
from route.models import Route

from utils.responsehelper import (RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_400_OBJECT_NOT_FOUND,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_200_DELETED,
                                  RESPONSE_200_UPDATED)

from utils.validators import way_data_validator



class WayView(View):
    """Class-based view for way model."""

    http_method_names = ['get', 'post', 'delete']

    def get(self, request, way_id=None):  # pylint: disable=R0201
        """
        Method for HTTP GET request

        :param request: client HttpRequest. Is required
        :type request: HttpRequest
        :param way_id: id of Way model
        :type way_id: int

        :return JsonResponse with way data and list with routes and status 200
                if parameters are good and way_id is specified,
                JsonResponse with all ways data and their lists of routes and staatus 200
                for request user if way_id is not specified
                or HttpRequest with error if parameters are bad.
        """
        user = request.user
        if not way_id:
            data = [way.get_way_with_routes() for way in user.ways.all()]

            return JsonResponse(data, status=200, safe=False)

        way = Way.get_by_id(obj_id=way_id)

        if not way:
            return RESPONSE_400_OBJECT_NOT_FOUND

        if not way.user == user:
            return RESPONSE_403_ACCESS_DENIED

        data = way.get_way_with_routes()
        return JsonResponse(data, status=200)

    def post(self, request, way_id):  # pylint: disable=R0201
        """
        Method for HTTP POST request

        :param request: client HttpRequest. Is required
        :type request: HttpRequest
        :param way_id: id of Way model
        :type way_id: int

        :return JsonResponse within way data and list with routes with status 200
                if parameters are good or HttpRequest with error if parameters are bad
        """
        data = request.body
        steps = data.get('steps')

        with transaction.atomic():

            if not way_data_validator(data):
                return RESPONSE_400_INVALID_DATA

            way = Way.create(user=request.user, name=data.get('name'))

            if not way:
                return RESPONSE_400_DB_OPERATION_FAILED

            routes = []
            position = 0

            for step in steps:
                route = _make_route_dict(step)
                if position == 0:
                    route['start_place'] = data.get('start_place')
                if position == len(steps)-1:
                    route['end_place'] = data.get('end_place')
                was_created = _create_route(way, position, **route)

                if not was_created:
                    return RESPONSE_400_INVALID_DATA
                position += 1
                routes.append(route)

            return JsonResponse({'way': way.to_dict(),
                                 'routes': routes}, status=201)

        return RESPONSE_400_DB_OPERATION_FAILED

    def delete(self, request, way_id):  # pylint: disable=R0201
        """
        Method for HTTP DELETE request

        :param request: client HttpRequest. Is required
        :type request: HttpRequest
        :param way_id: id of Way model
        :type way_id: int

        :return HTTPResponse with status 200 if parameters are good or
                HttpRequest with error if parameters are bad
        """
        user = request.user
        way = Way.get_by_id(obj_id=way_id)

        if not way:
            return RESPONSE_400_OBJECT_NOT_FOUND

        if not way.user == user:
            return RESPONSE_403_ACCESS_DENIED

        is_deleted = Way.delete_by_id(obj_id=way_id)

        if not is_deleted:
            return RESPONSE_400_DB_OPERATION_FAILED

        return RESPONSE_200_DELETED

    def put(self, request, way_id):  # pylint: disable=R0201
        """
        Method for HTTP PUT request

        :param request: client HttpRequest. Is required
        :type request: HttpRequest
        :param way_id: id of Way model
        :type way_id: int

        :return HTTPResponse with status 200 if parameters are good or
                HttpRequest with error if parameters are bad
        """
        user = request.user
        data = request.body

        way = Way.get_by_id(obj_id=way_id)

        if not way:
            return RESPONSE_400_OBJECT_NOT_FOUND

        if not way.user == user:
            return RESPONSE_403_ACCESS_DENIED

        data = {'name': data.get('name')}

        if not way_data_validator(data):
            return RESPONSE_400_DB_OPERATION_FAILED

        is_updated = way.update(**data)
        if not is_updated:
            return RESPONSE_400_DB_OPERATION_FAILED

        return RESPONSE_200_UPDATED


def _make_route_dict(step):
    """
    Function for creation dict from step data

    :param step: Step data. Is required
    :type step: dict

    :return dict with route information
    """
    route = {}

    dep = step.get('Dep')
    start_point = dep.get('Stn') or dep.get('Addr')

    start_place = {'longitude': start_point.get('x'),
                   'latitude': start_point.get('y')}

    arr = step.get('Arr')
    end_point = arr.get('Stn') or arr.get('Addr')

    end_place = {'longitude': end_point.get('x'),
                 'latitude': end_point.get('y')}

    route['start_place'] = start_place
    route['end_place'] = end_place
    route['time'] = str(isodate.parse_duration(step['Journey'].get('duration')))

    transport = dep.get('Transport')
    if transport and transport.get('name'):
        route['transport_id'] = transport.get('name')

    return route


def _create_route(way, position, **kwargs):
    """
        Function for route creation

        :param way: Way object. Is required
        :type way: object
        :param position: route position. Is required
        :type position: Int
        :param kwargs: Dict with route information.
        :type kwargs: dict

        :return True if route was created successfully or
                False if it was not
    """
    start_place = kwargs.get('start_place')
    end_place = kwargs.get('end_place')

    if isinstance(start_place, int):
        start_place = Place.get_by_id(start_place)
    else:
        start_place = Place.create(longitude=start_place['longitude'],
                                   latitude=start_place['latitude'])

    if isinstance(end_place, int):
        end_place = Place.get_by_id(end_place)
    else:
        end_place = Place.create(longitude=end_place['longitude'],
                                 latitude=end_place['latitude'])

    if not (start_place or end_place):
        return False

    time = kwargs.get('time')
    transport_id = kwargs.get('transport_id')
    route_obj = Route.create(way=way, start_place=start_place, end_place=end_place,
                             time=time, position=position, transport_id=transport_id)

    if not route_obj:
        return False
    return True
