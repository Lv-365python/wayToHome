"""The module that provide URL configuration for way app."""

from django.urls import re_path

from way.views import WayView

urlpatterns = [
    re_path('(?P<way_id>\d+)?/?$', WayView.as_view(), name='way'),
]
