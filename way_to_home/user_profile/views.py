"""This module that provides base logic for CRUD of user profile`s model objects."""

from django.http import HttpResponse, JsonResponse
from django.views import View
from utils.responsehelper import (RESPONSE_200_UPDATED,
                                  RESPONSE_400_EMPTY_JSON,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_404_OBJECT_NOT_FOUND)
from .models import UserProfile


class UserProfileView(View):
    "Class that handle HTTP requests for user_profile model."""

    def post(self, request, user_profile_id=None):
        """Handle the request to create a new user_profile object."""
        data = request.body
        if not data:
            return RESPONSE_400_EMPTY_JSON

        data = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name')
        }

        profile = UserProfile.create(user=request.user, **data)
        if not profile:
            return RESPONSE_400_DB_OPERATION_FAILED

        return JsonResponse(profile.to_dict(), status=201)
