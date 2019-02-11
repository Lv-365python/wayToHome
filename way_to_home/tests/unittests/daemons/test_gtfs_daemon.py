"""This module provides tests for GTFS daemon."""

from django.test import TestCase

from daemons.gtfs_daemon import GTFSDaemon
from unittest.mock import patch


class GTFSDaemonTestCase(TestCase):
    """TestCase for providing GTFS daemon testing."""

    def setUp(self):
        """Provide preparation data for testing of GTFS daemon."""
        self.frequency = 11
        self.gtfs_daemon = GTFSDaemon(self.frequency)

    def test_daemon_initialization(self):
        """Provide tests for proper initialization of daemon instance."""
        self.assertEqual(self.frequency, self.gtfs_daemon.frequency)
        self.assertIsNone(self.gtfs_daemon.pid)
        self.assertFalse(self.gtfs_daemon.is_processed)
        self.assertEqual('GTFSDaemon', self.gtfs_daemon.name)

    def test_daemon_start(self):
        """Provide tests for proper executing of `start` method."""
        self.gtfs_daemon.pid = None
        self.gtfs_daemon.is_processed = False

        self.gtfs_daemon.start()
        self.assertTrue(self.gtfs_daemon.is_processed)
        self.assertIsNotNone(self.gtfs_daemon.pid)

    def test_daemon_stop(self):
        """Provide tests for proper executing of `stop` method."""
        self.gtfs_daemon.is_processed = True

        self.gtfs_daemon.stop()
        self.assertFalse(self.gtfs_daemon.is_processed)

    @patch('daemons.gtfs_daemon.GTFSDaemon.start')
    @patch('daemons.gtfs_daemon.GTFSDaemon.stop')
    @patch('daemons.gtfs_daemon.GTFSDaemon.execute')
    def test_daemon_running(self, execute, stop, start):
        """Provide tests for execution of `running` method in case of `is_processed` is False."""
        self.gtfs_daemon.is_processed = False

        self.gtfs_daemon.run()
        self.assertTrue(start.called)
        self.assertTrue(stop.called)
        self.assertFalse(execute.called)

    @patch('utils.redishelper.RedisWorker.set')
    @patch('daemons.gtfs_daemon.load_file')
    @patch('daemons.gtfs_daemon.compile_file')
    def test_execute_success(self, compile_file, load_file, redis_set):
        """Provide tests for execute method in case of success."""
        redis_set.return_value = True
        load_file.return_value = 'loaded file'
        compile_file.return_value = 'compiled file'

        successful_executed = self.gtfs_daemon.execute()
        self.assertTrue(successful_executed)

    @patch('daemons.gtfs_daemon.load_file')
    def test_execute_fail_load_operation(self, load_file):
        """Provide tests for execute method in case of fail load file operation."""
        load_file.return_value = None

        successful_executed = self.gtfs_daemon.execute()
        self.assertFalse(successful_executed)

    @patch('daemons.gtfs_daemon.load_file')
    @patch('daemons.gtfs_daemon.compile_file')
    def test_execute_fail_compile_operation(self, compile_file, load_file):
        """Provide tests for execute method in case of fail compile file operation."""
        load_file.return_value = 'loaded file'
        compile_file.return_value = None

        successful_executed = self.gtfs_daemon.execute()
        self.assertFalse(successful_executed)

    @patch('utils.redishelper.RedisWorker.set')
    @patch('daemons.gtfs_daemon.load_file')
    @patch('daemons.gtfs_daemon.compile_file')
    def test_execute_fail_redis_set_operation(self, compile_file, load_file, redis_set):
        """Provide tests for execute method in case of fail Redis set operation."""
        redis_set.return_value = False
        load_file.return_value = 'loaded file'
        compile_file.return_value = 'compiled file'

        successful_executed = self.gtfs_daemon.execute()
        self.assertFalse(successful_executed)
