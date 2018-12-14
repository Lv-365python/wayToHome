"""This module implements class that represents the notification entity."""

from django.db import models, IntegrityError
from utils.abstract_models import AbstractModel
from way.models import Way


WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class Notification(AbstractModel):
    """Model for Notification entity."""

    way = models.ForeignKey(Way, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    week_day = models.PositiveSmallIntegerField()
    time = models.TimeField()

    def __str__(self):
        """Method that returns route instance as string."""

        return f'notification at: {WEEK[self.week_day]} {str(self.time)}'

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
    def create(cls, way=None, start_time=None, end_time=None, week_day=None, time=None):  # pylint: disable=arguments-differ
        """Method for object creation."""

        notification = cls()
        notification.start_time = start_time
        notification.end_time = end_time
        notification.week_day = week_day
        notification.time = time

        try:
            notification.way = way
            notification.save()
        except (ValueError, IntegrityError):
            notification = None

        return notification

    def update(self, way=None, start_time=None, end_time=None, week_day=None, time=None):  # pylint: disable=arguments-differ
        """Method for object updating."""

        if way:
            self.way = way
        if start_time:
            self.start_time = start_time
        if end_time:
            self.end_time = end_time
        if week_day:
            self.week_day = week_day
        if time:
            self.time = time
        self.save()
