"""Authentication views module"""
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from custom_user.models import CustomUser
from utils.jwttoken import create_token, decode_token
from utils.send_email import send_email
from way_to_home.settings import DOMAIN


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

