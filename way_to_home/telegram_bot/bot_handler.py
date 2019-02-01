"""This module provides handling of messages sent to telegram bot."""

from telegram_bot import bothelper
from custom_user.models import CustomUser

BOT = bothelper.BOT


@BOT.message_handler(commands=['start'])
def handle_start(message):
    """
        function that handles /start command to bot,
        received data : telegram message, with text property like '/start {user_id}'
    """
    user_id = (message.text.split()[-1])
    if not user_id == '/start' or user_id == 'start':
        user = CustomUser.get_by_id(int(user_id))
        if not user.telegram_id:
            user.update(telegram_id=message.chat.id)

    BOT.send_message(chat_id=message.chat.id, text='Сповіщення в телеграмі активовано.')


@BOT.message_handler(commands=['help'])
def handle_help(message):
    """function that handles /help command to telegram bot"""
    BOT.send_message(chat_id=message.chat.id,
                     text='В цьому чаті телеграму ви будете отримувати сповіщення,'
                          ' які ви зберегли на сайті WayToHome.')


if __name__ == '__main__':
    BOT.infinity_polling(True)
