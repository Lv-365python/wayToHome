"""This module implements class that represents the user entity."""

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models, IntegrityError


class User(AbstractBaseUser):
    """Model for User entity."""

    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    google_token = models.CharField(blank=True, max_length=255)
    phone_number = models.CharField(blank=True, max_length=15)

    def __str__(self):
        """Method that returns route instance as string."""

        return f"{self.email}"

    def to_dict(self):
        """Method that returns dict with object's attributes."""

        return {
            'id': self.id,
            'email': self.email,
            'phone_number': self.phone_number
        }

    @classmethod
    def create(cls, email=None, password=None, google_token=None, phone_number=None):  # pylint: disable=arguments-differ
        """Method for object creation."""

        user = cls()
        user.email = email
        user.password = password
        user.google_token = google_token
        user.phone_number = phone_number
        try:
            user.save()
            return user
        except (ValueError, IntegrityError):
            return None

    def update(self, email=None, password=None, google_token=None, phone_number=None):  # pylint: disable=arguments-differ
        """Method for object updating."""

        if email:
            self.email = email
        if password:
            self.password = password
        if google_token:
            self.google_token = google_token
        if phone_number:
            self.phone_number = phone_number
        self.save()
