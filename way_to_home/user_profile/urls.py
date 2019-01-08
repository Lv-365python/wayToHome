"""The module that provide URL configuration for place app."""

from django.urls import re_path

from .views import UserProfileView


urlpatterns = [
    re_path("(?P<profile_id>\d+)?/?$", UserProfileView.as_view(), name='profile'),
]
