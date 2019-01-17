"""This module implements class that represents the user entity."""


from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models, IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.db.utils import OperationalError


class CustomUser(AbstractBaseUser):
    """Model for User entity."""
    email = models.EmailField(max_length=64, unique=True)
    password = models.CharField(max_length=128)
    google_token = models.CharField(blank=True, max_length=255)
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

    def update(self, password=None, google_token=None, phone_number=None, is_active=None):
        """Method for object update."""
        with transaction.atomic():
            if password:
                self.set_password(password)
            if google_token:
                self.google_token = google_token
            if phone_number:
                self.phone_number = phone_number
            if is_active is not None:
                self.is_active = is_active
            try:
                self.save()
                return True
            except (ValueError, ValidationError, OperationalError):
                return False

    @classmethod
    def get_by_email(cls, email):
        """Method for returns user by email"""
        try:
            return cls.objects.get(email=email)
        except (ValueError, cls.DoesNotExist, OperationalError):
            pass

    @classmethod
    def get_by_id(cls, obj_id):
        """Method for returns user by id"""
        try:
            return cls.objects.get(id=obj_id)
        except (ValueError, cls.DoesNotExist, OperationalError):
            pass

    @classmethod
    def create(cls, email, password, google_token='', phone_number=''):
        """Method for object creation."""
        user = cls()
        user.email = email
        user.set_password(password)
        user.google_token = google_token
        user.phone_number = phone_number

        try:
            user.save()
            return user
        except (ValueError, IntegrityError, OperationalError):
            pass

    @classmethod
    def delete_by_id(cls, obj_id):
        """Delete user account found by id."""
        try:
            user = cls.objects.get(id=obj_id)
            user.delete()
            return True
        except (cls.DoesNotExist, OperationalError):
            return False
