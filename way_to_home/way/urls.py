from django.urls import path, re_path

from way.views import WayView

urlpatterns = [
    re_path('(?P<way_id>\d+)?/?$', WayView.as_view(), name='way'),
]
