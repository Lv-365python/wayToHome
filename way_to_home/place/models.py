"""This module implements class that represents the place entity."""

from user.models import User
from django.db import models, IntegrityError
from utils.abstract_models import AbstractModel


class Place(AbstractModel):
    """Model for place entity."""

    longitude = models.DecimalField()
    latitude = models.DecimalField()
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=255)
    stop_id = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, required=True)

    def __str__(self):
        """Method that returns route instance as string."""

        return f'{self.name}'

    def to_dict(self):
        """Method that returns dict with object's attributes."""

        return {
            'longitude': self.longitude,
            'latitude': self.latitude,
            'name': self.name,
            'address': self.address,
            'stop_id': self.stop_id,
            'user_id': self.user.id
        }

    @classmethod
    def create(cls, user, longitude=None, latitude=None, name=None, address=None, stop_id=None):  # pylint: disable=arguments-differ
        """Method for object creation."""

        place = cls()
        place.longitude = longitude
        place.latitude = latitude
        place.name = name
        place.address = address
        place.stop_id = stop_id
        place.user = user

        try:
            place.save()
        except (ValueError, IntegrityError):
            place = None

        return place

    def update(self, longitude=None, latitude=None, name=None, address=None, stop_id=None):  # pylint: disable=arguments-differ
        """Method for object updating."""

        if longitude:
            self.longitude = longitude
        if latitude:
            self.latitude = latitude
        if name:
            self.name = name
        if address:
            self.address = address
        if stop_id:
            self.stop_id = stop_id

        self.save()
