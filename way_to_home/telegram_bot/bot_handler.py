"""This module provides handling of messages sent to telegram bot."""

# pylint: disable=wrong-import-position

import os
import sys
import re

import django

SOURCE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SOURCE_PATH)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "way_to_home.settings")
django.setup()

from django.conf import settings
from telebot import TeleBot
from custom_user.models import CustomUser
from user_profile.models import UserProfile
from utils.loggerhelper import LOGGER
from telegram_bot.bot_helper import (get_user_id_by_access_token,
                                     remove_user_access_token,
                                     UNAUTHORIZED_ACCESS_MESSAGE)


BOT = TeleBot(token=settings.TELEGRAM_BOT_TOKEN)


@BOT.message_handler(commands=['start'])
def handle_start(message):
    """
    Function that handles /start command to bot,
    received data : telegram message, with text property like '/start {token}'
    """
    chat_id = message.chat.id

    if UserProfile.get_by_telegram_id(chat_id):
        BOT.send_message(chat_id=chat_id,
                         text='Сповіщення вже активовано.')
        return

    token = message.text.split()[-1]
    if re.search(r'^\/?start$', token):
        BOT.send_message(chat_id=chat_id,
                         text=UNAUTHORIZED_ACCESS_MESSAGE)
        return

    user_id = get_user_id_by_access_token(token)
    user = CustomUser.get_by_id(user_id)
    if not user:
        BOT.send_message(chat_id=chat_id,
                         text=UNAUTHORIZED_ACCESS_MESSAGE)
        return

    user.user_profile.update(telegram_id=chat_id)
    remove_user_access_token(user)
    BOT.send_message(chat_id=chat_id,
                     text=f'Сповіщення в телеграмі активовано для {user.email}.')

    LOGGER.info(f'Telegram was successfully activated for user with id={user.id}')


@BOT.message_handler(commands=['help'])
def handle_help(message):
    """Function that handles /help command to telegram bot"""
    BOT.send_message(chat_id=message.chat.id,
                     text='В цьому чаті телеграму ви будете отримувати сповіщення,'
                          ' які ви зберегли на сайті WayToHome.')


if __name__ == '__main__':
    BOT.infinity_polling(True)
