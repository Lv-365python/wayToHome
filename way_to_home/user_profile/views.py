"""This module that provides base logic for CRUD of user profile`s model objects."""

from django.http import JsonResponse
from django.views import View
from utils.validators import profile_validator
from utils.responsehelper import (RESPONSE_200_UPDATED,
                                  RESPONSE_400_EMPTY_JSON,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_400_OBJECT_NOT_FOUND,
                                  RESPONSE_400_INVALID_DATA)


class UserProfileView(View):
    "Class that handles HTTP requests for user_profile model."""
    http_method_names = ['get', 'put']

    def get(self, request):
        """Handle the request to retrieve a user_profile object."""
        user = request.user
        if not hasattr(user, 'user_profile'):
            return RESPONSE_400_OBJECT_NOT_FOUND

        profile = user.user_profile

        return JsonResponse(profile.to_dict(), status=200)

    def put(self, request):  # pylint: disable=R0201, R0911
        """Handle the request to update an existing user_profile object with appropriate id."""
        user = request.user

        if not hasattr(user, 'user_profile'):
            return RESPONSE_400_OBJECT_NOT_FOUND

        profile = user.user_profile
        data = request.body

        if not data:
            return RESPONSE_400_EMPTY_JSON

        data = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name')
        }

        if not profile_validator(data):
            return RESPONSE_400_INVALID_DATA

        is_updated = profile.update(**data)
        if not is_updated:
            return RESPONSE_400_DB_OPERATION_FAILED

        return RESPONSE_200_UPDATED
