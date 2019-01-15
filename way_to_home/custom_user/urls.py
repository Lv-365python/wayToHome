from django.urls import path, re_path, include

from custom_user.views import (signup,
                               registration_confirm,
                               log_in,
                               auth_google,
                               signin_google,
                               reset_password,
                               confirm_reset_password,
                               change_password)

urlpatterns = [
    path('register', signup, name='signup'),
    re_path(r'^activate/(?P<token>.+)$', registration_confirm, name='confirm_signup'),
    path('login', log_in, name='login_user'),
    path('auth_via_google', auth_google, name='auth_google'),
    path('signin_via_google', signin_google, name='sign_in_google'),
    path('profile', include('user_profile.urls')),
    path('reset_password', reset_password, name='reset_password'),
    re_path(r'^reset_password/(?P<token>.+)$', confirm_reset_password, name='confirm_reset_password'),
    path('change_password', change_password, name='change_password'),
]

