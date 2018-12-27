"""The module that provides creating and handling JWT tokens."""

import jwt
from django.conf import settings

SECRET_KEY = settings.JWT_TOKEN_KEY
ALGORITHM = settings.JWT_ALGORITHM


def create_token(data):
    """Function that creates JWT token with received date and certain expiration time."""
    token = jwt.encode(data, SECRET_KEY, ALGORITHM).decode("utf-8")
    return token


def decode_token(jwt_token):
    """Function that handle the received JWT token."""
    try:
        return jwt.decode(jwt_token, SECRET_KEY, ALGORITHM)
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        pass
