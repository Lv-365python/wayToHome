"""This module provides handling of messages send to telegram bot."""

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
from telegram_bot.helper import set_telegram_data

TOKEN = settings.TELEGRAM_BOT_TOKEN
BOT = TeleBot(token=TOKEN)


@BOT.message_handler(commands=['start'])
def handle_start(message):
    """
        function that handles /start command to bot,
        received data : telegram message, with text property like '/start {user_id}'
    """
    set_telegram_data(message)

    BOT.send_message(chat_id=message.chat.id, text='Сповіщення в телеграмі активовано.')


@BOT.message_handler(commands=['help'])
def handle_help(message):
    """function that handles /help command to telegram bot"""
    BOT.send_message(chat_id=message.chat.id,
                     text='В цьому чаті телеграму ви будете отримувати сповіщення,'
                          ' які ви зберегли на сайті WayToHome.')


if __name__ == '__main__':
    BOT.infinity_polling(True)
