"""This module that provides base logic for CRUD of way`s model objects."""

from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from way.models import Way
from place.models import Place
from route.models import Route


class WayView(View):
    """Class-based view for way model."""
    def post(self, request, way_id):  # pylint: disable=R0201
        """Method for POST."""
        # Add validator
        steps = request.body.get('gmaps_response')

        with transaction.atomic():
            # Add validator
            way = Way.create(user=request.user, name=request.body.get('name', ''))

            if not way:
                return HttpResponse('Failed to create way', status=400)

            routes = []
            position = 0

            for step in steps:
                # Add validators
                route = make_route_dict(step)

                start_place_data = route.get('start_place')
                start_place = Place.create(longitude=start_place_data['longitude'],
                                           latitude=start_place_data['latitude'])
                end_place_data = route.get('end_place')
                end_place = Place.create(longitude=end_place_data['longitude'],
                                         latitude=end_place_data['latitude'])
                time = route.get('time')
                transport_id = route.get('transport_id')
                Route.create(way=way, start_place=start_place, end_place=end_place,
                             time=time, position=position, transport_id=transport_id)
                position += 1

                routes.append(route)

        return JsonResponse({'way': way.to_dict(),
                             'routes': routes}, status=200)

    def delete(self, request, way_id):  # pylint: disable=R0201
        """Method for DELETE."""
        way = Way.get_by_id(obj_id=way_id)

        if not way:
            return HttpResponse('Way not found', status=404)

        if way.user.id != request.user.id:
            return HttpResponse('Access denied', status=403)

        if Way.delete_by_id(obj_id=way_id):
            return HttpResponse('Way was deleted', status=200)
        return HttpResponse('Way was not deleted', status=400)


def make_route_dict(step):
    """Function for creating dict with route information."""
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
