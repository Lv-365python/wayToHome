"""Authentication views module"""
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.db import transaction, DatabaseError, IntegrityError
from requests_oauthlib import OAuth2Session

from user_profile.models import UserProfile
from custom_user.models import CustomUser
from utils.jwttoken import create_token, decode_token
from utils.passwordreseting import send_email_password_update, send_successful_update_email

from utils.senderhelper import send_email
from utils.validators import credentials_validator, password_validator, email_validator

from utils.responsehelper import (RESPONSE_200_UPDATED,
                                  RESPONSE_400_EXISTED_EMAIL,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_200_ACTIVATED,
                                  RESPONSE_498_INVALID_TOKEN,
                                  RESPONSE_400_INVALID_EMAIL,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_400_INVALID_EMAIL_OR_PASSWORD,
                                  RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_201_ACTIVATE,
                                  RESPONSE_400_EMPTY_JSON,
                                  RESPONSE_200_OK,
                                  RESPONSE_201_CREATED,
                                  RESPONSE_400_OBJECT_NOT_FOUND)

from way_to_home.settings import (DOMAIN,
                                  CLIENT_ID,
                                  CLIENT_SECRET,
                                  REDIRECT_URI,
                                  AUTH_URL,
                                  TOKEN_URL,
                                  SCOPE,
                                  STATE)


@require_http_methods(["POST"])
def signup(request):
    """Function that provides user registration"""
    data = request.body
    credentials = {
        'email': data.get('email').lower().strip(),
        'password': data.get('password')
    }

    if not credentials_validator(credentials):
        return RESPONSE_400_INVALID_DATA

    user = CustomUser.create(**credentials)

    if not user:
        return RESPONSE_400_EXISTED_EMAIL

    token = create_token(data={'email': user.email})

    message = f'http://{DOMAIN}/api/v1/user/activate/{token}'
    mail_subject = 'Activate account'
    send_email(mail_subject, message, (user.email,))

    return RESPONSE_201_ACTIVATE


@require_http_methods(["GET"])
def registration_confirm(request, token):
    """Function that provides user activation"""
    data = decode_token(token)
    if not data:
        return RESPONSE_498_INVALID_TOKEN

    user = CustomUser.get_by_email(email=data.get('email'))
    if not user:
        return RESPONSE_400_INVALID_EMAIL
    try:
        with transaction.atomic():
            user.update(is_active=True)
            UserProfile.create(user)
            return RESPONSE_200_ACTIVATED
    except (DatabaseError, IntegrityError):
        return RESPONSE_400_DB_OPERATION_FAILED


@require_http_methods(["POST"])
def log_in(request):
    """Login of the existing user. Handles post and get requests."""
    data = request.body
    credentials = {
        'email': data.get('email').lower().strip(),
        'password': data.get('password')
    }

    if not credentials_validator(credentials):
        return RESPONSE_400_INVALID_DATA

    user = authenticate(**credentials)
    if not user:
        return RESPONSE_400_INVALID_EMAIL_OR_PASSWORD
    login(request, user=user)
    return RESPONSE_200_OK


@require_http_methods(["GET"])
def auth_google(request):
    """Function that provides getting url for confirmation access to user's data."""
    google_session = OAuth2Session(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI,
                                   state=STATE, scope=SCOPE)
    data = google_session.authorization_url(url=AUTH_URL, state=STATE)[0]
    if data:
        return redirect(data)

    return RESPONSE_403_ACCESS_DENIED


@require_http_methods(["GET"])
def signin_google(request):
    """Function that provides user registration or authorization via google."""
    google_session = OAuth2Session(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI,
                                   state=STATE, scope=SCOPE)
    authorization_code = request.GET.get('code')
    if not authorization_code:
        return RESPONSE_400_INVALID_DATA
    google_session.fetch_token(token_url=TOKEN_URL, client_secret=CLIENT_SECRET,
                               code=authorization_code)
    user_data = google_session.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    if user_data:
        user = CustomUser.get_by_email(user_data['email'])
        if user:
            login(request, user=user)
            return RESPONSE_200_ACTIVATED
        user = CustomUser.create(email=user_data.get('email'), password=user_data.get('email'))
        login(request, user=user)
        return RESPONSE_201_CREATED

    return RESPONSE_400_EMPTY_JSON


@require_http_methods(["POST"])
def reset_password(request):
    """Function that provides reset user password"""
    data = request.body
    email = data.get('email')
    if not email_validator(email):
        return RESPONSE_400_INVALID_EMAIL

    user = CustomUser.get_by_email(email=email)
    if not user:
        return RESPONSE_400_OBJECT_NOT_FOUND

    token = create_token(data={'email': user.email})
    send_email_password_update(user, token)

    return RESPONSE_200_OK


@require_http_methods(['PUT'])
def confirm_reset_password(request, token):
    """Function that provides confirm reset user password"""
    data = request.body
    new_password = data.get('new_password')
    confirm = decode_token(token)

    if not confirm:
        return RESPONSE_498_INVALID_TOKEN
    user = CustomUser.get_by_email(email=confirm.get('email'))

    if not user:
        return RESPONSE_400_OBJECT_NOT_FOUND

    if not password_validator(new_password) or user.check_password(new_password):
        return RESPONSE_400_INVALID_DATA

    is_updated = user.update(password=new_password)
    if not is_updated:
        return RESPONSE_400_DB_OPERATION_FAILED

    send_successful_update_email(user)
    return RESPONSE_200_UPDATED


@require_http_methods(["PUT"])
def change_password(request):
    """Function that provides change user password"""
    user = request.user
    data = request.body
    new_password = data.get('new_password')
    if (not password_validator(new_password) or not user.check_password(data.get('old_password'))
            or user.check_password(new_password)):
        return RESPONSE_400_INVALID_DATA

    is_updated = user.update(password=new_password)
    if not is_updated:
        return RESPONSE_400_DB_OPERATION_FAILED

    return RESPONSE_200_UPDATED
