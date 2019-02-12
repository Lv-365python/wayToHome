"""The module that provides creating and handling JSON web tokens."""

import jwt
from django.conf import settings

SECRET_KEY = settings.JWT_KEY
ALGORITHM = settings.JWT_ALGORITHM


def create_token(data):
    """Function that creates JWT with received date and certain expiration time."""
    token = jwt.encode(data, SECRET_KEY, ALGORITHM).decode("utf-8")
    return token


def decode_token(token):
    """Function that handle the received JWT."""
    try:
        return jwt.decode(token, SECRET_KEY, ALGORITHM)
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        pass
