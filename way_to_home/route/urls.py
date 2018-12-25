"""The module that provide URL configuration for route app."""

from django.urls import re_path

from .views import RouteView


urlpatterns = [
    re_path("(?P<route_id>\d+)?/?$", RouteView.as_view(), name='route'),
]
