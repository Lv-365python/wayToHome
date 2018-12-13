"""This module implements class that represents the way entity."""

from user.models import User
from django.db import models, IntegrityError
from utils.abstract_models import AbstractModel


class Way(AbstractModel):
    """Model for user profile entity."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Method that returns route instance as string."""

        return f'Way_id: {self.id}, user: {self.user}'

    def to_dict(self):
        """Method that returns dict with object's attributes."""

        return {
            'way_id': self.id,
            'user_id': self.user.id
        }

    @classmethod
    def create(cls, user):  # pylint: disable=arguments-differ
        """Method for object creation."""

        try:
            way = cls(user=user)
        except (ValueError, IntegrityError):
            way = None

        return way

    def update(self, **kwargs):  # pylint: disable=arguments-differ
        pass
