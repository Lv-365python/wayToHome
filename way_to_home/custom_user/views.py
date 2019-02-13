"""Authentication views module"""
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.db import transaction, DatabaseError, IntegrityError
from requests_oauthlib import OAuth2Session

from user_profile.models import UserProfile
from custom_user.models import CustomUser
from utils.jwthelper import create_token, decode_token
from utils.senderhelper import send_email
from utils.validators import (credentials_validator,
                              password_validator,
                              email_validator,
                              phone_validator)
from utils.responsehelper import (RESPONSE_200_OK,
                                  RESPONSE_200_UPDATED,
                                  RESPONSE_201_ACTIVATE,
                                  RESPONSE_400_EXISTED_EMAIL,
                                  RESPONSE_400_INVALID_DATA,
                                  RESPONSE_400_OBJECT_NOT_FOUND,
                                  RESPONSE_400_INVALID_EMAIL,
                                  RESPONSE_400_DB_OPERATION_FAILED,
                                  RESPONSE_400_INVALID_EMAIL_OR_PASSWORD,
                                  RESPONSE_400_EMPTY_JSON,
                                  RESPONSE_403_ACCESS_DENIED,
                                  RESPONSE_498_INVALID_TOKEN)
from way_to_home.settings import (DOMAIN,
                                  CLIENT_ID,
                                  CLIENT_SECRET,
                                  REDIRECT_URI,
                                  AUTH_URL,
                                  TOKEN_URL,
                                  SCOPE,
                                  STATE)


TTL_TOKEN = 60 * 60
TTL_USER_ID_COOKIE = 60 * 60 * 24 * 14


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

    ctx = {
        'domain': DOMAIN,
        'token': create_token(data={'email': user.email}, expiration_time=TTL_TOKEN)
    }

    mail_subject = 'Активувати акаунт'
    message = 'Активувати акаунт'
    html_message = render_to_string('emails/' + 'registration.html', ctx)

    send_email((user.email,), html_message, mail_subject, message)

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

        login(request, user=user)

        return HttpResponseRedirect('/')
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
    if not user or not user.is_active:
        return RESPONSE_400_INVALID_EMAIL_OR_PASSWORD

    login(request, user=user)

    if not data.get('remember_me'):
        request.session.set_expiry(0)

    response = RESPONSE_200_OK
    return response


@require_http_methods(['GET'])
def logout_user(request):
    """Logout the existing user"""
    logout(request)
    response = HttpResponseRedirect('/')
    return response


@require_http_methods(["GET"])
def auth_google(request):
    """Function that provides getting url for confirmation access to user's data."""
    google_session = OAuth2Session(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI,
                                   state=STATE, scope=SCOPE)
    data = google_session.authorization_url(url=AUTH_URL, state=STATE)[0]
    if data:
        return JsonResponse({"url": data}, status=200)
    return RESPONSE_403_ACCESS_DENIED


@require_http_methods(["GET"])
def signin_google(request):
    """Function that provides user registration or authorization via google."""
    google_session = OAuth2Session(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI,
                                   state=STATE, scope=SCOPE)
    authorization_code = request.GET.get('code')
    if not authorization_code:
        return RESPONSE_403_ACCESS_DENIED
    google_session.fetch_token(token_url=TOKEN_URL, client_secret=CLIENT_SECRET,
                               code=authorization_code)
    user_data = google_session.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    if user_data:
        user = CustomUser.get_by_email(user_data['email'])
        if not user:
            try:
                with transaction.atomic():
                    user = CustomUser.create(email=user_data.get("email"),
                                             password=user_data.get("email"))
                    user.update(is_active=True)
                    UserProfile.create(user=user)

            except (DatabaseError, IntegrityError):
                return RESPONSE_400_DB_OPERATION_FAILED

        login(request, user=user)
        response = HttpResponseRedirect('/')
        response.set_cookie('picture', value=user_data.get('picture'))
        return response
    return RESPONSE_400_EMPTY_JSON


@require_http_methods(["DELETE"])
def delete_account(request):
    """Function that provides deleting user account."""
    user = request.user
    is_deleted = CustomUser.delete_by_id(obj_id=user.id)
    if not is_deleted:
        return RESPONSE_400_DB_OPERATION_FAILED

    logout(request)
    response = HttpResponseRedirect('/')
    return response


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

    ctx = {
        'domain': DOMAIN,
        'token': create_token(data={'email': user.email}, expiration_time=TTL_TOKEN)
    }

    mail_subject = 'Скинути пароль'
    message = 'Скинути пароль'
    html_message = render_to_string('emails/' + 'change_password_link.html', ctx)

    send_email((user.email,), html_message, mail_subject, message)

    return RESPONSE_200_OK


@require_http_methods(['PUT'])
def confirm_reset_password(request, token):
    """Function that provides confirm reset user password"""
    confirm = decode_token(token)
    if not confirm:
        return RESPONSE_498_INVALID_TOKEN
    data = request.body
    new_password = data.get('new_password')

    user = CustomUser.get_by_email(email=confirm.get('email'))

    if not user:
        return RESPONSE_400_OBJECT_NOT_FOUND

    if not password_validator(new_password) or user.check_password(new_password):
        return RESPONSE_400_INVALID_DATA

    is_updated = user.update(password=new_password)

    if not is_updated:
        return RESPONSE_400_DB_OPERATION_FAILED

    mail_subject = 'Успішне відновлення паролю'
    message = 'Успішне відновлення паролю'
    html_message = render_to_string('emails/' + 'update_password.html')

    send_email((user.email,), html_message, mail_subject, message)

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


@require_http_methods(["GET"])
def get_info(request):
    """Function that provides retrieving of user info"""
    user = request.user

    return JsonResponse(user.to_dict(), status=200)


@require_http_methods(["PUT"])
def change_phone(request):
    """Function that provides updating of users phone number"""
    user = request.user
    phone = request.body.get('phone')
    if not phone_validator(phone):
        return RESPONSE_400_INVALID_DATA

    is_updated = user.update(phone_number=phone)

    if not is_updated:
        return RESPONSE_400_DB_OPERATION_FAILED

    return RESPONSE_200_UPDATED
