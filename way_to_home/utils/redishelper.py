"""This module provides helper functionality for redis interaction."""

from redis import Redis, RedisError

__all__ = ["REDIS_HELPER"]


class RedisWorker:
    """Provide functionality for redis interaction."""
    __instance = None
    __redis = Redis()

    def __new__(cls):
        """
        Creates a new instance if not exist, otherwise
        returns reference to already created instance.
        """
        if cls.__instance is None:
            cls.__instance = super(RedisWorker, cls).__new__(cls)

        return cls.__instance

    def set(self, key, value, cache_time=None):
        """Sets data in redis database with specifying the expire time."""
        try:
            self.__redis.set(key, value, cache_time)
        except RedisError:
            return False

        return True

    def get(self, key):
        """Retrieves object from redis database by `key`."""
        try:
            obj = self.__redis.get(key)
        except RedisError:
            return None

        return obj


REDIS_HELPER = RedisWorker()
