from django.urls import path, include


urlpatterns = [
    path('<int:way_id>/notification/', include('notification.urls')),
]

