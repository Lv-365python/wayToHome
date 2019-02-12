"""This module provides helping functions for telegram bot."""

import pickle
import os
import sys
import django

# pylint: disable=wrong-import-position

SOURCE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SOURCE_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "way_to_home.settings")
django.setup()

from django.conf import settings
from telebot import TeleBot
from utils.redishelper import REDIS_HELPER

UNAUTHORIZED_ACCESS_MESSAGE = 'Для активації сповіщень через телеграм' \
                              ' необхідно скористатись посиланням на нашому сайті.'
TELEGRAM_REDIS_KEY = 'telegram'
TOKEN = settings.TELEGRAM_BOT_TOKEN
BOT = TeleBot(token=TOKEN)


def get_access_tokens():
    """Retrieve dictionary with pairs of user id and token from redis"""
    telegram_pickled = REDIS_HELPER.get(TELEGRAM_REDIS_KEY)
    telegram_data = pickle.loads(telegram_pickled) if telegram_pickled else {}
    return telegram_data


def set_access_tokens(data):
    """Retrieve dictionary with pairs of user id and token from redis"""
    telegram_pickled = pickle.dumps(data)
    return REDIS_HELPER.set(TELEGRAM_REDIS_KEY, telegram_pickled)


def remove_user_access_token(user):
    """Function to remove redis record about telegram access token"""
    telegram_data = get_access_tokens()
    if not telegram_data.pop(user.id, False):
        return False
    set_access_tokens(telegram_data)
    return True


def get_user_id_by_access_token(token_check):
    """find user_id by access token in redis"""
    for user_id, token in get_access_tokens().items():
        if token == token_check:
            return user_id
    return None
