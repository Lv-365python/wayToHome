"""This module provides handling of messages sent to telegram bot."""

from telegram_bot import bot_helper
from custom_user.models import CustomUser
from user_profile.models import UserProfile
BOT = bot_helper.BOT


@BOT.message_handler(commands=['start'])
def handle_start(message):
    """
        Function that handles /start command to bot,
        received data : telegram message, with text property like '/start {user_id}'
    """
    if UserProfile.get_by_telegram_id(message.chat.id):
        BOT.send_message(chat_id=message.chat.id,
                         text='сповіщення вже активовано')
        return

    token = (message.text.split()[-1])
    if token in('/start', 'start'):
        BOT.send_message(chat_id=message.chat.id,
                         text=bot_helper.UNAUTHORIZED_ACCESS_MESSAGE)
    else:
        user_id = bot_helper.get_user_id_by_access_token(token)
        user = CustomUser.get_by_id(user_id)
        if not user:
            BOT.send_message(chat_id=message.chat.id,
                             text=bot_helper.UNAUTHORIZED_ACCESS_MESSAGE)
            return

        user.user_profile.update(telegram_id=message.chat.id)
        bot_helper.remove_user_access_token(user)
        BOT.send_message(chat_id=message.chat.id,
                         text=f'Сповіщення в телеграмі активовано для {user.email}.')


@BOT.message_handler(commands=['help'])
def handle_help(message):
    """Function that handles /help command to telegram bot"""
    BOT.send_message(chat_id=message.chat.id,
                     text='В цьому чаті телеграму ви будете отримувати сповіщення,'
                          ' які ви зберегли на сайті WayToHome.')


if __name__ == '__main__':
    BOT.infinity_polling(True)
