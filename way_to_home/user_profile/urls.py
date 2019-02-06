"""The module that provide URL configuration for place app."""

from django.urls import path

from user_profile.views import UserProfileView, put_access_token, update_telegram_id


urlpatterns = [
    path('', UserProfileView.as_view(), name='profile'),
    path('/telegram_access_token', put_access_token, name='telegram_redis'),
    path('/telegram_id', update_telegram_id, name='telegram_id')
]
