"""The module that provide URL configuration for way app."""

from django.urls import re_path, path, include

from way.views import WayView

urlpatterns = [
    re_path('(?P<way_id>\d+)?/?$', WayView.as_view(), name='way'),
    path("<int:way_id>/notification/", include('notification.urls')),
    path("<int:way_id>/route/", include('route.urls')),
]
