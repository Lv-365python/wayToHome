"""The module that provide URL configuration for notification app."""

from django.urls import re_path

from .views import NotificationView


urlpatterns = [
    re_path("(?P<notification_id>\d+)?/?$", NotificationView.as_view(), name='notification'),
]
