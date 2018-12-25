"""Authentication views module"""
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from requests_oauthlib import OAuth2Session

from custom_user.models import CustomUser
from utils.jwttoken import create_token, decode_token
from utils.send_email import send_email
from way_to_home.settings import (DOMAIN, CLIENT_ID, CLIENT_SECRET,
                                  REDIRECT_URI, AUTH_URL, TOKEN_URL, SCOPE, STATE)


@require_http_methods(["POST"])
def signup(request):
    """Function that provides user registration"""
    data = request.body
    email = data.get('email').lower().strip()
    password = data.get('password')
    user = CustomUser.create(
        email=email,
        password=password
    )

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
    email = data.get('email').lower().strip()
    password = data.get('password')
    user = authenticate(email=email, password=password)
    if not user:
        return HttpResponse('invalid credentials', status=400)
    login(request, user=user)
    return HttpResponse('operation was successful provided', status=200)


@require_http_methods(["GET"])
def auth_google(request):
    """Function that provides getting url for confirmation access to user's data."""
    google = OAuth2Session(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI, state=STATE, scope=SCOPE)
    data = google.authorization_url(url=AUTH_URL, state=STATE)[0]
    if data:
        return redirect(data)
    return HttpResponse("Failed", status=400)


@require_http_methods(["GET"])
def signin_google(request):
    """Function that provides user registration or authorization via google."""
    google = OAuth2Session(client_id=CLIENT_ID, redirect_uri=REDIRECT_URI, state=STATE, scope=SCOPE)
    try:
        code = request.GET["code"]
    except ValueError:
        return HttpResponse("Failed", status=400)
    google.fetch_token(token_url=TOKEN_URL, client_secret=CLIENT_SECRET, code=code,
                       authorization_response='/api/v1/user/sign_in')
    user_data = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
    if user_data:
        user = CustomUser.get_by_email(user_data['email'])
        if user:
            login(request, user=user)
            return HttpResponse('User was successfully activated', status=200)
        user = CustomUser.create(email=user_data.get("email"), password=user_data.get("email"))
        login(request, user=user)
        return HttpResponse("User was successfully created", status=201)

    return HttpResponse("Failed", status=400)
