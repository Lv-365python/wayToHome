from django.db import models
from abc import abstractmethod


class AbstractModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_by_id(cls, id):
        try:
            obj = cls.objects.get(id=id)
        except cls.DoesNotExist:
            obj = None
        return obj

    @classmethod
    def delete_by_id(cls, id):
        try:
            obj = cls.objects.get(id=id)
            obj.delete()
            return True
        except cls.DoesNotExist:
            return False

    @staticmethod
    @abstractmethod
    def create(*args, **kwargs):
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass
