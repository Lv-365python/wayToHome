"""This module implements class that represents the way entity."""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError
from django.db.utils import OperationalError
from custom_user.models import CustomUser
from utils.abstract_models import AbstractModel
from utils.utils import LOGGER


class Way(AbstractModel):
    """Model for user profile entity."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ways')
    name = models.CharField(max_length=128, blank=True)

    def __str__(self):
        """Method that returns route instance as string."""
        return f'Way id: {self.id}, user id: {self.user.id}'

    def to_dict(self):
        """Method that returns dict with object's attributes."""
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user.id
        }

    def get_way_with_routes(self):
        """Method that returns dictionary with way's info, and all of the way's routes"""
        way = self.to_dict()
        way['routes'] = [route.to_dict() for route in self.routes.all()]
        return way

    @classmethod
    def create(cls, user, name=None):  # pylint: disable=arguments-differ
        """Method for object creation."""
        way = cls()
        way.name = name if name is not None else ''

        try:
            way.user = user
            way.save()
            return way
        except (ValueError, IntegrityError, OperationalError) as err:
            LOGGER.error(f'Unsuccessful way creating. {err}')

    def get_first_route(self):
        """Return first route of way."""
        try:
            return self.routes.get(position=0)
        except (ObjectDoesNotExist, OperationalError):
            pass
