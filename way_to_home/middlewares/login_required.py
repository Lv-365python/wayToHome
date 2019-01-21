"""This module implements custom middlewares."""

import json

from utils.responsehelper import (RESPONSE_400_INVALID_DATA,
                                  RESPONSE_403_USER_NOT_AUTHENTICATED,
                                  RESPONSE_403_ACCESS_DENIED)


GUESTS_PATHS = [
    '/api/v1/user/login',
    '/api/v1/user/register',
    '/api/v1/user/activate',
    '/api/v1/user/auth_via_google',
    '/api/v1/user/signin_via_google',
    '/api/v1/user/reset_password',
    '/api/v1/user/confirm_reset_password'
]


class LoginRequiredMiddleware:  # pylint: disable=too-few-public-methods
    """
    The сustom middleware that provides JSON check, performs authentication
    validations in case if the path is not available for anonymous users.
    """

    def __init__(self, get_response):
        """Initialize middleware instance."""
        self.get_response = get_response

    def __call__(self, request):
        """Provide JSON check and authentication validations."""
        if not request.path_info.startswith('/api'):
            response = self.get_response(request)
            return response

        if request.method in ['POST', 'PUT']:
            try:
                request._body = json.loads(request.body)  # pylint: disable=protected-access
            except json.JSONDecodeError:
                return RESPONSE_400_INVALID_DATA

        for path in GUESTS_PATHS:
            if request.path_info.startswith(path):
                if request.user.is_authenticated:
                    return RESPONSE_403_ACCESS_DENIED
                response = self.get_response(request)
                return response

        if not request.user.is_authenticated:
            return RESPONSE_403_USER_NOT_AUTHENTICATED

        response = self.get_response(request)
        return response
