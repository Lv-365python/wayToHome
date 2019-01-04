"""
Notification view module
================

This module that provides base logic for CRUD of notification`s model objects.
"""

from django.http import JsonResponse
from django.views import View

from notification.models import Notification

from utils.validators import notification_data_validator
from utils.responsehelper import (RESPONSE_200_UPDATED,
                                  RESPONSE_200_DELETED,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_404_OBJECT_NOT_FOUND,
                                  )
from way.models import Way


class NotificationView(View):
    """
    Notification view that handles GET, POST, PUT, DELETE requests and provides
    appropriate operations with notification model.
    """
    def get(self, request, way_id, notification_id=None):
        """ Method that handles GET request. """

        user = request.user
        way = Way.get_by_id(obj_id=way_id)

        if not way:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if not user == way.user:
            return RESPONSE_403_ACCESS_DENIED

        if not notification_id:
            data = [notification.to_dict() for notification
                    in way.notifications.all().order_by('week_day')]

            return JsonResponse(data, status=200, safe=False)

        notification = Notification.get_by_id(obj_id=notification_id)
        if not notification:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if not way == notification.way:
            return RESPONSE_403_ACCESS_DENIED

        return JsonResponse(notification.to_dict(), status=200)

    def put(self, request, way_id, notification_id=None):  # pylint: disable=R0201, R0911
        """ Method that handles PUT request. """
        user = request.user
        data = request.body
        way = Way.get_by_id(obj_id=way_id)

        if not (way and notification_id):
            return RESPONSE_404_OBJECT_NOT_FOUND

        if not user == way.user:
            return RESPONSE_403_ACCESS_DENIED

        notification = Notification.get_by_id(obj_id=notification_id)
        if not notification:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if not way == notification.way:
            return RESPONSE_403_ACCESS_DENIED

        data = {
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'week_day': data.get('week_day'),
            'time': data.get('time')
        }

        if not notification_data_validator(data, update=True):
            return RESPONSE_400_INVALID_DATA

        is_updated = notification.update(**data)
        if not is_updated:
            return RESPONSE_400_DB_OPERATION_FAILED

        return RESPONSE_200_UPDATED

    def post(self, request, way_id, notification_id=None):
        """ Method that handles POST request. """
        user = request.user
        data = request.body
        way = Way.get_by_id(obj_id=way_id)

        if not way:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if not user == way.user:
            return RESPONSE_403_ACCESS_DENIED

        data = {
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'week_day': data.get('week_day'),
            'time': data.get('time'),
            'way': way,
        }

        if not notification_data_validator(data):
            return RESPONSE_400_INVALID_DATA

        notification = Notification.create(**data)
        if not notification:
            return RESPONSE_400_DB_OPERATION_FAILED

        return JsonResponse(notification.to_dict(), status=201)

    def delete(self, request, way_id, notification_id=None):  # pylint: disable=R0201
        """ Method that handles DELETE request. """
        user = request.user
        way = Way.get_by_id(obj_id=way_id)

        if not (way and notification_id):
            return RESPONSE_404_OBJECT_NOT_FOUND

        if not user == way.user:
            return RESPONSE_403_ACCESS_DENIED

        notification = Notification.get_by_id(obj_id=notification_id)
        if not notification:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if not way == notification.way:
            return RESPONSE_403_ACCESS_DENIED

        is_deleted = Notification.delete_by_id(notification_id)
        if not is_deleted:
            return RESPONSE_400_DB_OPERATION_FAILED

        return RESPONSE_200_DELETED
