"""This module that provides base logic for CRUD of way`s model objects."""

from datetime import datetime, timedelta
from django.views.generic import View
from django.http import JsonResponse
from django.db import transaction
from django.db import DatabaseError
from way.models import Way
from place.models import Place
from route.models import Route

from utils.responsehelper import (RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_400_OBJECT_NOT_FOUND,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_200_DELETED)

from utils.validators import way_data_validator, route_data_validator


class WayView(View):
    """Class-based view for way model."""

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

        try:
            with transaction.atomic():
                if not way_data_validator(data):
                    return RESPONSE_400_INVALID_DATA

                way = Way.create(user=request.user, name=data.get('name'))

                if not way:
                    return RESPONSE_400_DB_OPERATION_FAILED

                position = 0

                for step in steps:

                    route = _make_route_dict_from_google_maps(step)

                    if not route_data_validator(route):
                        return RESPONSE_400_INVALID_DATA

                    if position == 0:
                        route['start_place'] = data.get('start_place')
                    if position == len(steps)-1:
                        route['end_place'] = data.get('end_place')

                    was_created = _create_route(way, position, **route)

                    if not was_created:
                        return RESPONSE_400_INVALID_DATA
                    position += 1

                data = way.get_way_with_routes()
                return JsonResponse(data, status=201)

        except DatabaseError:
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


def _make_route_dict_from_google_maps(step):
    """
    Function for creation dict from google maps api
    :param step: Step data. Is required
    :type step: dict
    :return dict with route information
    """
    route = {}
    start_place = {'longitude': step['start_location']['lng'],
                   'latitude': step['start_location']['lat']}
    route['start_place'] = start_place

    end_place = {'longitude': step['end_location']['lng'],
                 'latitude': step['end_location']['lat']}
    route['end_place'] = end_place

    time = timedelta(seconds=step['duration']['value'])
    route['time'] = datetime.strptime(str(time), '%H:%M:%S').time()

    if step.get('transit'):
        short_name = step['transit']['line']['short_name']
        vehicle_type = step['transit']['line']['vehicle']['type']

        if vehicle_type == 'TROLLEYBUS':
            pre_name = 'Тр'
        elif vehicle_type == 'TRAM':
            pre_name = 'Т'
        elif vehicle_type == 'SHARE_TAXI':
            pre_name = 'А'
        elif vehicle_type == 'BUS':
            pre_name = 'А'
            short_name = short_name.replace('A', '')

        short_name = short_name.rjust(2, '0')
        route['transport_name'] = pre_name + short_name

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
        start_place.pk = None
        start_place.user_id = None
        start_place.save()
    else:
        start_place = Place.create(longitude=start_place['longitude'],
                                   latitude=start_place['latitude'])

    if isinstance(end_place, int):
        end_place = Place.get_by_id(end_place)
        end_place.pk = None
        end_place.user_id = None
        end_place.save()
    else:
        end_place = Place.create(longitude=end_place['longitude'],
                                 latitude=end_place['latitude'])

    if not start_place or not end_place:
        return False

    time = kwargs.get('time')
    transport_name = kwargs.get('transport_name')
    route_obj = Route.create(way=way, start_place=start_place, end_place=end_place,
                             time=time, position=position, transport_name=transport_name)

    if not route_obj:
        return False
    return True
