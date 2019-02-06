"""This module that provides base logic for CRUD of user profile`s model objects."""

from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods

from telegram_bot.bothelper import (get_access_tokens,
                                    set_access_tokens,
                                    remove_user_access_token)
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
            'last_name': data.get('last_name'),
        }

        if not profile_validator(data):
            return RESPONSE_400_INVALID_DATA

        is_updated = profile.update(**data)
        if not is_updated:
            return RESPONSE_400_DB_OPERATION_FAILED

        return RESPONSE_200_UPDATED


@require_http_methods(["PUT"])
def put_access_token(request):
    """Set telegram access token to redis as value with key of user id"""
    user = request.user
    if not hasattr(user, 'user_profile'):
        return RESPONSE_400_OBJECT_NOT_FOUND

    token = request.body.get('token')
    telegram_data = get_access_tokens()
    telegram_data[user.id] = token
    if not set_access_tokens(telegram_data):
        return RESPONSE_400_DB_OPERATION_FAILED

    return RESPONSE_200_UPDATED


@require_http_methods(["PUT"])
def update_telegram_id(request):
    """
        Update telegram id in user profile,
        separated form common put to add ability to process None in body
    """
    user = request.user
    if not hasattr(user, 'user_profile'):
        return RESPONSE_400_OBJECT_NOT_FOUND

    profile = user.user_profile
    telegram_id = request.body.get('telegram_id')
    if telegram_id is None:
        remove_user_access_token(user)
        profile.update(telegram_id=None)
        return RESPONSE_200_UPDATED

    if not isinstance(telegram_id, int):
        return RESPONSE_400_INVALID_DATA

    is_update = profile.update(telegram_id=telegram_id)
    if not is_update:
        return RESPONSE_400_DB_OPERATION_FAILED

    return RESPONSE_200_UPDATED
