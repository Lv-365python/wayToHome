"""
Abstract model
===========
This module implements abstract class.
"""

from abc import abstractmethod

from django.db import models, IntegrityError, transaction
from django.db.utils import OperationalError


class AbstractModel(models.Model):
    """Model that describes abstract entity."""

    class Meta:
        abstract = True

    @classmethod
    def get_by_id(cls, obj_id):
        """
        Return object, found by id.
        """
        try:
            obj = cls.objects.get(id=obj_id)
        except (cls.DoesNotExist, OperationalError):
            obj = None
        return obj

    @classmethod
    def delete_by_id(cls, obj_id):
        """
        Delete object, found by id.
        """
        try:
            obj = cls.objects.get(id=obj_id)
            obj.delete()
            return True
        except (cls.DoesNotExist, OperationalError):
            return False

    @classmethod
    @abstractmethod
    def create(cls, **kwargs):
        """Create object."""

    def update(self, **kwargs):
        """Update object parameters."""
        with transaction.atomic():
            for key, value in kwargs.items():
                if value:
                    setattr(self, key, value)
            try:
                self.save()
                return True
            except (ValueError, IntegrityError, OperationalError):
                return False

    @abstractmethod
    def to_dict(self):
        """Return dictionary with object's info."""
