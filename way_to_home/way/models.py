"""This module implements class that represents the way entity."""

from custom_user.models import CustomUser
from django.db import models, IntegrityError


class Way(models.Model):
    """Model for user profile entity."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Method that returns route instance as string."""
        return f'Way_id: {self.id}, user_id: {self.user_id}'

    def to_dict(self):
        """Method that returns dict with object's attributes."""
        return {
            'way_id': self.id,
            'user_id': self.user_id
        }

    @classmethod
    def create(cls, user):  # pylint: disable=arguments-differ
        """Method for object creation."""
        try:
            way = cls(user=user)
            return way
        except (ValueError, IntegrityError):
            pass
