"""
Notification view module
================

This module that provides base logic for CRUD of notification`s model objects.
"""

from django.views import View
from django.http import HttpResponse, JsonResponse

from notification.models import Notification
from way.models import Way


class NotificationView(View):
    """
    Notification view that handles GET, POST, PUT, DELETE requests and provides
    appropriate operations with notification model.
    """
    def get(self, request, way_id, notification_id=None):
        """ Method that handles GET request. """
        user = request.user
        way = Way.get_by_id(way_id)

        if not way:
            return HttpResponse('way is not found', status=400)

        if way.user != user:
            return HttpResponse('permission denied', status=403)

        if not notification_id:
            data = [notification.to_dict() for notification in way.notifications.all()]
            return JsonResponse(data, status=200, safe=False)

        notification = Notification.get_by_id(notification_id)
        if not notification:
            return HttpResponse('Notification not found', status=400)

        if notification.way != way:
            return HttpResponse('permission denied', status=403)

        return JsonResponse(notification.to_dict(), status=200)

    def put(self, request, way_id, notification_id=None):  # pylint: disable=R0201
        """ Method that handles PUT request. """
        user = request.user
        data = request.body
        way = Way.get_by_id(obj_id=way_id)

        if not notification_id:
            return HttpResponse('obj_id are not received', status=400)

        notification = Notification.get_by_id(obj_id=notification_id)

        if not (notification or way):
            return HttpResponse('failed, obj not found', status=400)

        if not (way == notification.way or user == way.user):
            return HttpResponse('permission denied', status=403)

        data = {
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'week_day': data.get('week_day'),
            'time': data.get('time'),
            'way': way
        }

        # if not notification_data_validator(data, update=True):
        #     return HttpResponse('invalid data', status=400)

        is_updated = notification.update(**data)
        if not is_updated:
            return HttpResponse('Notification is not updated', status=400)

        return HttpResponse('database is updated', status=200)

    def post(self, request, way_id, notification_id=None):
        """ Method that handles POST request. """
        user = request.user
        data = request.body
        way = Way.get_by_id(obj_id=way_id)

        if not way:
            return HttpResponse('way is not found', status=400)

        if not way.user == user:
            return HttpResponse('Permission denied', status=403)

        data = {
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'week_day': data.get('week_day'),
            'time': data.get('time'),
            'way': way
        }

        # if not notification_data_validator(data):
        #     return HttpResponse('invalid data', status=400)

        notification = Notification.create(**data)
        if not notification:
            return HttpResponse('Notification is not created', status=400)

        return JsonResponse(notification.to_dict(), status=201)

    def delete(self, request, way_id, notification_id=None):  # pylint: disable=R0201
        """ Method that handles DELETE request. """
        user = request.user
        way = Way.get_by_id(obj_id=way_id)

        if not notification_id:
            return HttpResponse('obj_ids are not received', status=400)

        notification = Notification.get_by_id(obj_id=notification_id)

        if not (notification or way):
            return HttpResponse('failed, obj not found', status=400)

        if not (way == notification.way or user == way.user):
            return HttpResponse('permission denied', status=403)

        is_deleted = Notification.delete_by_id(notification_id)
        if not is_deleted:
            return HttpResponse('database operation is failed', status=400)

        return HttpResponse('notification is deleted', status=200)
