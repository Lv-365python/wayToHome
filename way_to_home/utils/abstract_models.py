"""
Abstract model
===========
This module implements abstract class.
"""

from abc import abstractmethod

from django.db import models, IntegrityError, transaction
from django.db.utils import OperationalError

from utils.utils import LOGGER


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
            return cls.objects.get(id=obj_id)
        except (cls.DoesNotExist, OperationalError) as err:
            LOGGER.error(f'Certain {cls.__name__} with id={obj_id} does not exist. {err}')

    @classmethod
    def delete_by_id(cls, obj_id):
        """
        Delete object, found by id.
        """
        try:
            obj = cls.objects.get(id=obj_id)
            obj.delete()
            return True
        except (cls.DoesNotExist, OperationalError) as err:
            LOGGER.error(f'Certain {cls.__name__} with id={obj_id} does not delete. {err}')
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
            except (ValueError, IntegrityError, OperationalError) as err:
                LOGGER.error(f'Unsuccessful object parameters update with id={self.id}. {err}')
                return False

    @abstractmethod
    def to_dict(self):
        """Return dictionary with object's info."""
