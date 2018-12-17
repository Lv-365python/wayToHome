"""This module implements class that represents the user entity."""

import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models, IntegrityError



class CustomUser(AbstractBaseUser):
    """Model for User entity."""
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    google_token = models.CharField(null=True, max_length=255, unique=True)
    email_token = models.UUIDField(default=uuid.uuid4)
    phone_number = models.CharField(blank=True, max_length=15)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = BaseUserManager()

    def __str__(self):
        """Method that returns route instance as string."""
        return f'{self.id} {self.email}'

    def to_dict(self):
        """Method that returns dict with object's attributes."""
        return {
            'id': self.id,
            'email': self.email,
            'phone_number': self.phone_number
        }

    @classmethod
    def create(cls, email=None, password=None, google_token=None,
               email_token=None, phone_number=''):
        """Method for object creation."""
        user = cls()
        user.email = email
        user.set_password(password)
        user.google_token = google_token
        user.email_token = email_token
        user.phone_number = phone_number
        try:
            user.save()
            return user
        except (ValueError, IntegrityError):
            pass
