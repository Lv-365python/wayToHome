"""This module implements custom middlewares."""

import json

from django.http import HttpResponse


GUESTS_PATHS = [
    '/api/v1/user/login',
    '/api/v1/user/register',
    '/api/v1/user/activate'
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
        if request.method in ['POST', 'PATCH', 'PUT']:
            try:
                request._body = json.loads(request.body)  # pylint: disable=protected-access
            except json.JSONDecodeError:
                return HttpResponse('invalid json received', status=400)

        for path in GUESTS_PATHS:
            if request.path_info.startswith(path):
                if request.user.is_authenticated:
                    return HttpResponse('access denied for authenticated user', status=400)
                response = self.get_response(request)
                return response

        if not request.user.is_authenticated:
            return HttpResponse('access denied for unauthenticated user', status=403)

        response = self.get_response(request)
        return response
