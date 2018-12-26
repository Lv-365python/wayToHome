"""This module that provides base logic for CRUD of way`s model objects."""

from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from way.models import Way
from place.models import Place
from route.models import Route


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

        way = user.ways.filter(id=way_id).first()

        if not way:
            return HttpResponse('Object not found', status=400)

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
        # Add validator
        steps = request.body.get('gmaps_response')

        with transaction.atomic():
            # Add validator
            way = Way.create(user=request.user, name=request.body.get('name'))

            if not way:
                return HttpResponse('Failed to create way', status=400)

            routes = []
            position = 0

            for step in steps:
                # Add validators
                route = make_route_dict(step)
                was_created = create_route(way, position, **route)

                if not was_created:
                    return HttpResponse('Bad request', status=400)
                position += 1
                routes.append(route)

        return JsonResponse({'way': way.to_dict(),
                             'routes': routes}, status=201)

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
        way = user.ways.filter(id=way_id).first()

        if not way:
            return HttpResponse('Way not found', status=400)

        is_deleted = Way.delete_by_id(obj_id=way_id)

        if is_deleted:
            return HttpResponse('Way was deleted', status=200)
        return HttpResponse('Way was not deleted', status=400)

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

        way = user.ways.filter(id=way_id).first()
        if not way:
            return HttpResponse('Object not found', status=400)

        data = {'name': data.get('name')}
        # if not way_data_validator(data):
        # return HttpResponse('Database operation has failed', status=400)

        is_updated = way.update(**data)
        if not is_updated:
            return HttpResponse('Database operation has failed', status=400)

        return HttpResponse('Object was successfully updated', status=200)


def make_route_dict(step):
    """
    Function for creation dict from step data

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

    route['time'] = step['duration']['value']

    if step.get('transit_details'):
        transport_id = step['transit_details']['line']['short_name']
        route['transport_id'] = transport_id

    return route


def create_route(way, position, **kwargs):
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
    places = {'start_place': kwargs.get('start_place'),
              'end_place': kwargs.get('end_place')}

    start_place = Place.create(longitude=places['start_place']['longitude'],
                               latitude=places['start_place']['latitude'])
    end_place = Place.create(longitude=places['end_place']['longitude'],
                             latitude=places['end_place']['latitude'])

    if not (start_place or end_place):
        return False

    time = kwargs.get('time')
    transport_id = kwargs.get('transport_id')
    route_obj = Route.create(way=way, start_place=start_place, end_place=end_place,
                             time=time, position=position, transport_id=transport_id)

    if not route_obj:
        return False
    return True
