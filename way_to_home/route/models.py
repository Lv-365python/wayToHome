"""This module implements class that represents the route entity."""

from django.db import models, IntegrityError
from utils.abstract_models import AbstractModel
from way.models import Way
from place.models import Place


class Route(AbstractModel):
    """Model for Route entity."""
    way = models.ForeignKey(Way, on_delete=models.CASCADE, related_name='routes')
    start_place = models.ForeignKey(Place,
                                    related_name='start_routes',
                                    on_delete=models.CASCADE)
    end_place = models.ForeignKey(Place,
                                  related_name='end_routes',
                                  on_delete=models.CASCADE)
    time = models.TimeField()
    transport_id = models.PositiveIntegerField(null=True)
    position = models.PositiveSmallIntegerField()

    def __str__(self):
        """Method that returns route instance as string."""
        return f'route from: {self.start_place.id} to {self.end_place.id}'

    def to_dict(self):
        """Method that returns dict with object's attributes."""
        return {
            'id': self.id,
            'time': self.time,
            'transport_id': self.transport_id,
            'position': self.position,
            'way': self.way.id,
            'start_place': self.start_place.id,
            'end_place': self.end_place.id

        }

    @classmethod
    def create(cls, way, start_place, end_place, time,  # pylint: disable=arguments-differ
               position, transport_id=None):
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
            pass
