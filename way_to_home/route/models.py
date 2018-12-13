"""This module implements class that represents the route entity."""

from django.db import models, IntegrityError
from utils.abstract_models import AbstractModel
from way.models import Way
from place.models import Place


class Route(AbstractModel):
    """Model for Route entity."""

    way = models.ForeignKey(Way, on_delete=models.CASCADE)
    start_place = models.ForeignKey(Place, on_delete=models.CASCADE)
    end_place = models.ForeignKey(Place, on_delete=models.CASCADE)
    time = models.TimeField()
    transport_id = models.PositiveIntegerField(null=True)
    position = models.PositiveSmallIntegerField()

    def __str__(self):
        """Method that returns route instance as string."""

        return f'route from place: {self.start_place.id} to place {self.end_place.id}'

    def to_dict(self):
        """Method that returns dict with object's attributes."""

        return {
            'id': self.id,
            'time': self.time,
            'transport_id': self.transport_id,
            'position': self.position,
            'way': self.way.id,
            'start_place': self.start_place,
            'end_place': self.end_place

        }

    @classmethod
    def create(cls, way=None, start_place=None, end_place=None,  # pylint: disable=arguments-differ
               time=None, transport_id=None, position=None):
        """Method for object creation."""

        route = cls()
        route.time = time
        route.transport_id = transport_id
        route.position = position

        try:
            route.way = way
            route.start_place = start_place
            route.end_place = end_place
            route.save()
            return route
        except (ValueError, IntegrityError):
            return None

    def update(self, way=None, start_place=None, end_place=None,  # pylint: disable=arguments-differ
               time=None, transport_id=None, position=None):
        """Method for object updating."""

        if way:
            self.way = way
        if start_place:
            self.start_place = start_place
        if end_place:
            self.end_place = end_place
        if time:
            self.time = time
        if transport_id:
            self.transport_id = transport_id
        if position:
            self.position = position
        self.save()
