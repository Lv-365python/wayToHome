"""The module that provides creating and handling JSON web tokens."""

import jwt
from django.conf import settings
from django.utils import timezone

SECRET_KEY = settings.JWT_KEY
ALGORITHM = settings.JWT_ALGORITHM


def create_token(data, expiration_time=None, not_before_time=None):
    """Function that creates JWT with received date and certain expiration time."""
    try:
        if expiration_time:
            exp = int(timezone.now().timestamp()) + expiration_time
            data['exp'] = exp

        if not_before_time:
            nbf = int(timezone.now().timestamp()) + not_before_time
            data['nbf'] = nbf

        token = jwt.encode(data, SECRET_KEY, ALGORITHM).decode("utf-8")
        return token
    except TypeError:
        pass


def decode_token(token):
    """Function that handle the received JWT."""
    try:
        return jwt.decode(token, SECRET_KEY, ALGORITHM)
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        pass
