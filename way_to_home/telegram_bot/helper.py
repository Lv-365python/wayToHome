"""This module provides helpers functions for telegram bot."""

import pickle
from utils.redishelper import REDIS_HELPER as redis


def set_telegram_data(message):
    """function that receives telegram message object, and saves user id + chat id pair to redis"""
    pickled_telegram_data = redis.get('telegram')
    telegram_data = pickle.loads(pickled_telegram_data)

    user_id = int(message.text.split()[-1])
    telegram_data[user_id] = message.chat.id
    pickled_telegram_data = pickle.dumps(telegram_data)
    redis.set('telegram', pickled_telegram_data)
