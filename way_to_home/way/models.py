"""This module implements class that represents the way entity."""

from django.db import models, IntegrityError
from custom_user.models import CustomUser
from utils.abstract_models import AbstractModel
from utils.custom_manager import CustomManager


class Way(AbstractModel):
    """Model for user profile entity."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ways')
    name = models.CharField(max_length=128, blank=True)

    objects = CustomManager()

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

    @classmethod
    def create(cls, user, name=''):  # pylint: disable=arguments-differ
        """Method for object creation."""
        way = cls()
        way.name = name

        try:
            way.user = user
            return way
        except (ValueError, IntegrityError):
            pass
