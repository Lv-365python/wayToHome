"""This module that provides base logic for CRUD of user profile`s model objects."""

from django.http import HttpResponse, JsonResponse
from django.views import View
from utils.responsehelper import (RESPONSE_200_UPDATED,
                                  RESPONSE_200_DELETED,
                                  RESPONSE_400_EMPTY_JSON,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_404_OBJECT_NOT_FOUND)
from .models import UserProfile


class UserProfileView(View):
    "Class that handles HTTP requests for user_profile model."""

    def get(self, request, user_profile_id=None):
        """Handle the request to retrieve a user_profile object."""
        user = request.user

        if not user_profile_id:
            profile = user.user_profile

            if not profile:
                return RESPONSE_404_OBJECT_NOT_FOUND

            return JsonResponse(profile.to_dict, status=200)

        profile = UserProfile.get_by_id(user_profile_id)

        if not profile:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if profile.user and profile.user != user:
            return RESPONSE_403_ACCESS_DENIED

        return JsonResponse(profile.to_dict, status=200)

    def put(self, request, user_profile_id=None):  # pylint: disable=R0201, R0911
        """Handle the request to update an existing user_profile object with appropriate id."""
        user = request.user

        if not user_profile_id:
            return HttpResponse('object id is not received', status=400)

        data = request.body

        if not data:
            return RESPONSE_400_EMPTY_JSON

        profile = UserProfile.get_by_id(user_profile_id)

        if not profile:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if profile.user and profile.user != user:
            return RESPONSE_403_ACCESS_DENIED

        data = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name')
        }

        is_updated = profile.update(**data)
        if not is_updated:
            return RESPONSE_400_DB_OPERATION_FAILED

        return RESPONSE_200_UPDATED

    def delete(self, request, user_profile_id=None):  # pylint: disable=R0201
        """Handle the request to delete user_profile object with appropriate id."""
        user = request.user

        if not user_profile_id:
            return HttpResponse('object id is not received', status=400)

        profile = UserProfile.get_by_id(user_profile_id)

        if not profile:
            return RESPONSE_404_OBJECT_NOT_FOUND

        if profile.user and profile.user != user:
            return RESPONSE_403_ACCESS_DENIED

        is_deleted = UserProfile.delete_by_id(user_profile_id)
        if not is_deleted:
            return RESPONSE_400_DB_OPERATION_FAILED

        return RESPONSE_200_DELETED
