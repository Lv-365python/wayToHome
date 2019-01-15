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

    def set(self, key, value, cache_time):
        """Sets data in redis database with specifying the expire time."""
        return self.redis.set(key, value, cache_time)

    def get(self, key):
        """Retrieve data from redis database."""
        return self.redis.get(key)


REDIS_HELPER = RedisWorker()
