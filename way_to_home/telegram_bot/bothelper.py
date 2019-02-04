"""This module provides helping functions for telegram bot."""

import os
import sys
import django

# pylint: disable=wrong-import-position

SOURCE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SOURCE_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "way_to_home.settings")
django.setup()

from django.conf import settings
from telebot import TeleBot, apihelper

TOKEN = settings.TELEGRAM_BOT_TOKEN
BOT = TeleBot(token=TOKEN)


def send_telegram_message(text, user):
    """This function sends telegram message with given text to user"""
    chat_id = user.user_profile.telegram_id
    if not chat_id:
        return False
    try:
        BOT.send_message(chat_id=chat_id, text=text)
    except apihelper.ApiException:
        return False
    return True
