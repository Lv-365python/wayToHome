"""
Abstract model
===========
This module implements abstract class.
"""

from django.db import models
from abc import abstractmethod


class AbstractModel(models.Model):
    """Model that describes abstract entity."""
    class Meta:
        abstract = True

    @classmethod
    def get_by_id(cls, id):
        """
        Return object, found by id.
        """
        try:
            obj = cls.objects.get(id=id)
        except cls.DoesNotExist:
            obj = None
        return obj

    @classmethod
    def delete_by_id(cls, id):
        """
        Delete object, found by id.
        """
        try:
            obj = cls.objects.get(id=id)
            obj.delete()
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    @abstractmethod
    def create(cls, **kwargs):
        """Create object."""

    @abstractmethod
    def update(self, **kwargs):
        """Update object parameters."""

    @abstractmethod
    def to_dict(self):
        """Return dictionary with object's info."""
