"""Authentication views module"""
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from requests_oauthlib import OAuth2Session

from custom_user.models import CustomUser
from utils.jwttoken import create_token, decode_token
from utils.passwordreseting import send_email_password_update, send_successful_update_email
from utils.responsehelper import (RESPONSE_200_OK,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_498_INVALID_TOKEN,
                                  RESPONSE_400_OBJECT_NOT_FOUND,
                                  RESPONSE_200_UPDATED,
                                  RESPONSE_400_DB_OPERATION_FAILED, RESPONSE_400_INVALID_EMAIL)
from utils.send_email import send_email
from utils.validators import (registration_validator,
                              login_validator,
                              password_validator, email_validator)
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

    if not registration_validator(credentials):
        return HttpResponse('invalid data', status=400)

    user = CustomUser.create(**credentials)

    if not user:
        return HttpResponse('received email is already exist', status=400)

    token = create_token(data={'email': user.email})

    message = f'http://{DOMAIN}/api/v1/user/activate/{token}'
    mail_subject = 'Activate account'
    send_email(mail_subject, message, (user.email,))
    msg = 'Please confirm your email address to complete the registration'

    return HttpResponse(msg, status=201)


@require_http_methods(["GET"])
def registration_confirm(request, token):
    """Function that provides user activation"""
    data = decode_token(token)
    if not data:
        return HttpResponse('invalid or expired token', status=498)

    user = CustomUser.get_by_email(email=data.get('email'))
    if not user:
        return HttpResponse('received email is not valid', status=400)

    is_updated = user.update(is_active=True)
    if not is_updated:
        return HttpResponse('database operations is failed', status=400)

    return HttpResponse('user was successfully activated', status=200)


@require_http_methods(["POST"])
def log_in(request):
    """Login of the existing user. Handles post and get requests."""

    data = request.body
    credentials = {
        'email': data.get('email').lower().strip(),
        'password': data.get('password')
    }

    if not login_validator(credentials):
        return HttpResponse('invalid data', status=400)

    user = authenticate(**credentials)
    if not user:
        return HttpResponse('invalid credentials', status=400)
    login(request, user=user)
    return HttpResponse('operation was successful provided', status=200)


@require_http_methods(["GET"])
def auth_google(request):
    """Function that provides getting url for confirmation access to user's data."""
    google_session = OAuth2Session(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI,
                                   state=STATE, scope=SCOPE)
    data = google_session.authorization_url(url=AUTH_URL, state=STATE)[0]
    if data:
        return redirect(data)
    return HttpResponse("Access denied", status=403)


@require_http_methods(["GET"])
def signin_google(request):
    """Function that provides user registration or authorization via google."""
    google_session = OAuth2Session(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI,
                                   state=STATE, scope=SCOPE)
    authorization_code = request.GET.get("code")
    if not authorization_code:
        return HttpResponse("Code doesn't exist", status=400)
    google_session.fetch_token(token_url=TOKEN_URL, client_secret=CLIENT_SECRET,
                               code=authorization_code)
    user_data = google_session.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    if user_data:
        user = CustomUser.get_by_email(user_data['email'])
        if user:
            login(request, user=user)
            return HttpResponse('User was successfully activated', status=200)
        user = CustomUser.create(email=user_data.get("email"), password=user_data.get("email"))
        login(request, user=user)
        return HttpResponse("User was successfully created", status=201)

    return HttpResponse("User's data is empty", status=400)


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

    if not password_validator(new_password):
        return RESPONSE_400_INVALID_DATA

    if not user.check_password(new_password):
        is_updated = user.update(password=new_password)

        if not is_updated:
            return RESPONSE_400_DB_OPERATION_FAILED

        send_successful_update_email(user)
        return RESPONSE_200_UPDATED

    return RESPONSE_400_INVALID_DATA


@require_http_methods(["PUT"])
def change_password(request):
    """Function that provides change user password"""
    user = request.user
    data = request.body
    new_password = data.get('new_password')
    if not user.check_password(data.get('old_password')) or not password_validator(new_password):
        return RESPONSE_400_INVALID_DATA
    if not user.check_password(new_password):
        is_updated = user.update(password=new_password)
        if not is_updated:
            return RESPONSE_400_DB_OPERATION_FAILED
        return RESPONSE_200_UPDATED
    return RESPONSE_400_INVALID_DATA
