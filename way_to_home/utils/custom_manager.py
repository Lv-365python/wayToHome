"""
Custom Manager
===========
This module implements custom manager.
"""


from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class CustomManager(models.Manager):
    """Manager that provides database query operations to model"""

    def get_by_id(self, obj_id):
        """
        Return object, found by id.
        """
        try:
            obj = self.get(id=obj_id)
        except ObjectDoesNotExist:
            obj = None
        return obj

    def delete_by_id(self, obj_id):
        """
        Delete object, found by id.
        """
        try:
            obj = self.get(id=obj_id)
            obj.delete()
            return True
        except ObjectDoesNotExist:
            return False
