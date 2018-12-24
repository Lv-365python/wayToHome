from django.urls import path, re_path

from custom_user.views import signup, registration_confirm, log_in, auth_google, signin_google

urlpatterns = [
    path('register', signup, name='signup'),
    re_path(r'^activate/(?P<token>.+)$', registration_confirm, name='confirm_signup'),
    path('login', log_in, name='login_user'),
    path('auth_via_google', auth_google, name='login_google'),
    path('signin_via_google', signin_google, name='signup_google'),
]
