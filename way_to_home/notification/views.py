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
    def get(self, request, notification_id=None):
        """ Method that handles GET request. """
        user = request.user
        if not user:
            return HttpResponse('login to view notifications', status=400)

        if not notification_id:

            data = []
            for way in user.ways.all():
                for notific in Notification.objects.all():
                    if way == notific.way:
                        data.append(notific.to_dict())

            return JsonResponse(data, status=200, safe=False)

        notification = Notification.get_by_id(notification_id)
        if not notification:
            return HttpResponse('Notification not found', status=400)

        return JsonResponse(notification.to_dict(), status=200)

    def put(self, request, notification_id=None):  # pylint: disable=R0201
        """ Method that handles PUT request. """

        if not notification_id:
            return HttpResponse('object id is not received', status=400)

        data = request.body
        if not data:
            return HttpResponse('database operation is failed, data not found', status=404)

        user = request.user
        if not user:
            return HttpResponse('permission denied', status=400)

        notification = Notification.get_by_id(notification_id)
        if not notification:
            return HttpResponse('database operation is failed, notification not found', status=404)

        if user != notification.way.user:
            return HttpResponse('permission denied', status=400)

        data = {
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'week_day': data.get('week_day'),
            'time': data.get('time'),
            'way': data.get('way')
        }

        # if not notification_data_validator(data, update=True):
        #     return HttpResponse('invalid data', status=400)

        is_updated = notification.update(**data)

        if not is_updated:
            return HttpResponse('Notification is not updated', status=400)

        return HttpResponse('database is updated', status=200)

    def post(self, request, notification_id=None):
        """ Method that handles POST request. """
        if not request.user:
            return HttpResponse('permission denied', status=400)

        data = request.body
        if not data:
            return HttpResponse('Invalid data', status=400)

        data = {
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'week_day': data.get('week_day'),
            'time': data.get('time'),
            'way': Way.get_by_id(obj_id=data.get('way'))
        }

        # if not notification_data_validator(data):
        #     return HttpResponse('invalid data', status=400)

        notification = Notification.create(**data)

        if not notification:
            return HttpResponse('Notification is not created', status=400)

        return JsonResponse(notification.to_dict(), status=200)

    def delete(self, request, notification_id=None):  # pylint: disable=R0201
        """ Method that handles DELETE request. """
        user = request.user
        if not user:
            return HttpResponse('permission denied', status=400)

        notification = Notification.get_by_id(notification_id)
        if not notification:
            return HttpResponse('database operation is failed, notification not found', status=404)

        if user != notification.way.user:
            return HttpResponse('permission denied', status=400)

        is_deleted = Notification.delete_by_id(notification_id)
        if not is_deleted:
            return HttpResponse('database operation is failed', status=400)

        return HttpResponse('notification is deleted', status=200)
