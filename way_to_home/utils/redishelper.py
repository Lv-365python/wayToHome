"""This module provides helper functionality for redis interaction."""

import redis


class RedisWorker:
    """Provide functionality for redis interaction."""
    instance = None
    redis = redis.Redis()

    def __new__(cls):
        """
        Creates a new instance if not exist, otherwise
        returns reference to already created instance.
        """
        if cls.instance is None:
            cls.instance = super(RedisWorker, cls).__new__(cls)

        return cls.instance

    def set(self, key, value, cache_time=None):
        """Sets data in redis database with specifying the expire time."""
        try:
            self.redis.set(key, value, cache_time)
        except redis.RedisError:
            return False

        return True

    def get(self, key):
        """Retrieves object from redis database by `key`."""
        try:
            obj = self.redis.get(key)
        except redis.RedisError:
            return None

        return obj


REDIS_HELPER = RedisWorker()
