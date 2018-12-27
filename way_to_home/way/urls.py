"""The module that provide URL configuration for route app."""

from django.urls import path, include


urlpatterns = [
    path("<int:way_id>/route/", include('route.urls')),
]
