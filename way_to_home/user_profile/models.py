"""This module implements class that represents the user profile entity."""

from django.db import models, IntegrityError
from django.db.utils import OperationalError
from custom_user.models import CustomUser
from utils.abstract_models import AbstractModel


class UserProfile(AbstractModel):
    """Model for user profile entity."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    first_name = models.CharField(max_length=64, blank=True)
    last_name = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """Method that returns route instance as string."""
        return f'{self.first_name} {self.last_name}'

    def to_dict(self):
        """Method that returns dict with object's attributes."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_id': self.user.id
        }

    @classmethod
    def create(cls, user, first_name='', last_name=''):  # pylint: disable=arguments-differ
        """Method for object creation."""
        user_profile = cls()
        user_profile.first_name = first_name
        user_profile.last_name = last_name

        try:
            user_profile.user = user
            user_profile.save()
            return user_profile
        except (ValueError, IntegrityError, OperationalError):
            pass
