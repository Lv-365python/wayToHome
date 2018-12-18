"""This module implements class that represents the notification entity."""

from django.db import models, IntegrityError
from utils.abstract_models import AbstractModel
from way.models import Way


class Notification(AbstractModel):
    """Model for Notification entity."""
    way = models.ForeignKey(Way, on_delete=models.CASCADE, related_name='notifications')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    week_day = models.PositiveSmallIntegerField()
    time = models.TimeField()

    def __str__(self):
        """Method that returns route instance as string."""
        return f'notification at: {self.week_day} {str(self.time)}'

    def to_dict(self):
        """Method that returns dict with object's attributes."""
        return {
            'id': self.id,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'week_day': self.week_day,
            'time': self.time,
            'way': self.way_id
        }

    @classmethod
    def create(cls, way, start_time, end_time, week_day, time):  # pylint: disable=arguments-differ
        """Method for object creation."""
        notification = cls()
        notification.start_time = start_time
        notification.end_time = end_time
        notification.week_day = week_day
        notification.time = time

        try:
            notification.way = way
            notification.save()
            return notification
        except (ValueError, IntegrityError):
            pass
