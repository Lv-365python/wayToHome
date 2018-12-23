"""
Notification view module
================

This module that provides base logic for CRUD of notification`s model objects.
"""

from django.views import View
from django.http import HttpResponse, JsonResponse

from notification.models import Notification


class NotificationView(View):
    """
    Notification view that handles GET, POST, PUT, DELETE requests and provides
    appropriate operations with notification model.
    """
    def get(self, request, notification_id=None): # pylint: disable=R0201
        """ Method that handles GET request. """

        user = request.user
        print(user)
        # TODO user

        if not notification_id:
            notifications = user.notifications.all()

            data = [notification.to_dict() for notification in notifications]

            return JsonResponse(data, status=200, safe=False)

        notification = Notification.get_by_id(notification_id)

        if not notification:
            return HttpResponse('Notification not found', status=400)



        return JsonResponse(notification.to_dict(), status=200)

    def put(self, request, notification_id=None):
        """ Method that handles PUT request. """

        if not notification_id:
            return HttpResponse('object id is not received', status=400)

        data = request.body
        if not data:
            return HttpResponse('database operation is failed, data not found', status=404)

        notification = Notification.get_by_id(notification_id)
        if not notification:
            return HttpResponse('database operation is failed, notification not found', status=404)

        data = {
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'week_day': data.get('week_day'),
            'time': data.get('time'),
            'way': data.get('way')
        }

        # if not notification_data_validator(data, update=True):
        #     return HttpResponse('invalid data', status=400)

        is_updated = Notification.update(**data)

        if not is_updated:
            return HttpResponse('Notification is not updated', status=400)

        return HttpResponse('database is updated', status=200)

    def post(self, request): # pylint: disable=R0201
        """ Method that handles POST request. """

        data = request.body
        if not data:
            return HttpResponse('Invalid data', status=400)

        data = {
            'start_time': data.get('start_time'),
            'end_time': data.get('end_time'),
            'week_day': data.get('week_day'),
            'time': data.get('time'),
            'way': data.get('way')
        }

        # if not notification_data_validator(data):
        #     return HttpResponse('invalid data', status=400)

        notification = Notification.create(**data)

        if not notification:
            return HttpResponse('Notification is not created', status=400)

        return JsonResponse(notification.to_dict(), status=200)

    def delete(self, request, notification_id=None):  # pylint: disable=R0201
        """ Method that handles DELETE request. """
        if not notification_id:
            return HttpResponse('object id is not received', status=400)

        notification = Notification.get_by_id(notification_id)
        if not notification:
            return HttpResponse('database operation is failed, notification not found', status=404)

        is_deleted = Notification.delete_by_id(notification_id)
        if not is_deleted:
            return HttpResponse('database operation is failed', status=400)

        return HttpResponse('notification is deleted', status=200)

