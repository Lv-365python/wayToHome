"""This module provides tests for Redis worker."""

from redis import RedisError

from django.test import TestCase
from unittest.mock import patch

from utils.redishelper import RedisWorker


class RedisWorkerTestCase(TestCase):
    """TestCase for providing Redis worker testing."""

    def setUp(self):
        """Method that provides preparation before testing Redis worker."""
        self.redis_helper = RedisWorker()
        self.key = 'test key'
        self.value = 'test value'

    @patch('redis.Redis.set')
    def test_set_success(self, redis_set):
        """Provide tests for `set` method in case of success."""
        redis_set.return_value = True
        successful_inserted = self.redis_helper.set(self.key, self.value)
        self.assertTrue(successful_inserted)

    @patch('redis.Redis.set')
    def test_set_redis_error(self, redis_set):
        """Provide tests for `set` method in case of raised RedisError."""
        redis_set.side_effect = RedisError
        successful_inserted = self.redis_helper.set(self.key, self.value)
        self.assertFalse(successful_inserted)

    @patch('redis.Redis.get')
    def test_get_success(self, redis_get):
        """Provide tests for `set` method in case of success."""
        redis_get.return_value = self.value
        expected_value = self.redis_helper.get(self.key)
        self.assertEqual(self.value, expected_value)

    @patch('redis.Redis.get')
    def test_get_redis_error(self, redis_get):
        """Provide tests for `get` method in case of raised RedisError."""
        redis_get.side_effect = RedisError
        expected_value = self.redis_helper.get(self.key)
        self.assertFalse(expected_value)

    def test_new_success(self):
        """Provide test for proper executions of `__new__` method."""
        new_worker = RedisWorker()
        self.assertIs(self.redis_helper, new_worker)

        RedisWorker._RedisWorker__instance = None
        new_worker = RedisWorker()
        self.assertIsNot(self.redis_helper, new_worker)
