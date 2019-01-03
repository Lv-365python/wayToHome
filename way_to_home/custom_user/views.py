"""Authentication views module"""
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from requests_oauthlib import OAuth2Session


from custom_user.models import CustomUser
from utils.jwttoken import create_token, decode_token
from utils.send_email import send_email
from utils.validators import registration_validator, login_validator

from utils.responsehelper import (RESPONSE_400_EXISTED_EMAIL,
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
                                  RESPONSE_201_CREATED)

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

    is_updated = user.update(is_active=True)
    if not is_updated:
        return RESPONSE_400_DB_OPERATION_FAILED

    return RESPONSE_200_ACTIVATED


@require_http_methods(["POST"])
def log_in(request):
    """Login of the existing user. Handles post and get requests."""

    data = request.body
    credentials = {
        'email': data.get('email').lower().strip(),
        'password': data.get('password')
    }

    if not login_validator(credentials):
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
    authorization_code = request.GET.get("code")
    if not authorization_code:
        return HttpResponse("Code not received", status=400)
    google_session.fetch_token(token_url=TOKEN_URL, client_secret=CLIENT_SECRET,
                               code=authorization_code)
    user_data = google_session.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    if user_data:
        user = CustomUser.get_by_email(user_data['email'])
        if user:
            login(request, user=user)
            return RESPONSE_200_ACTIVATED
        user = CustomUser.create(email=user_data.get("email"), password=user_data.get("email"))
        login(request, user=user)
        return RESPONSE_201_CREATED

    return RESPONSE_400_EMPTY_JSON
