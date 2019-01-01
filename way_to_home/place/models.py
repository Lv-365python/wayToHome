"""This module implements class that represents the place entity."""

from django.db import models, IntegrityError
from custom_user.models import CustomUser
from utils.abstract_models import AbstractModel


class Place(AbstractModel):
    """Model for place entity."""
    longitude = models.DecimalField(decimal_places=6, max_digits=9)
    latitude = models.DecimalField(decimal_places=6, max_digits=9)
    name = models.CharField(max_length=64, blank=True)
    address = models.CharField(max_length=255, blank=True)
    stop_id = models.PositiveSmallIntegerField(null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='places')

    def __str__(self):
        """Method that returns route instance as string."""
        return f'{self.longitude}, {self.latitude}'

    def to_dict(self):
        """Method that returns dict with object's attributes."""
        return {
            'id': self.id,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'name': self.name,
            'address': self.address,
            'stop_id': self.stop_id,
            'user_id': self.user.id
        }

    @classmethod
    def create(cls, longitude, latitude, address=None, name=None, user=None, stop_id=None):  # pylint: disable=arguments-differ
        """Method for object creation."""
        place = cls()
        place.longitude = longitude
        place.latitude = latitude
        place.name = name if name is not None else ''
        place.address = address if address is not None else ''
        place.stop_id = stop_id

        try:
            place.user = user
            place.save()
            return place
        except (ValueError, IntegrityError):
            pass
