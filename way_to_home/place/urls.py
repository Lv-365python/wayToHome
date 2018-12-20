"""The module that provide URL configuration for place app."""

from django.urls import re_path

from .views import PlaceView


urlpatterns = [
    re_path('place/(?P<obj_id>\d+)?', PlaceView.as_view(), name='place'),
]
