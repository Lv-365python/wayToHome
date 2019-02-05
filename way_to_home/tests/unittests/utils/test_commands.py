"""This module provides tests for custom commands."""

from unittest.mock import patch

from django.test import TestCase

from utils.management.commands.prepare_data import Command


class CustomCommandsTestCase(TestCase):
    """TestCase for providing custom commands testing."""

    @patch('builtins.print')
    @patch('utils.management.commands.prepare_data.prepare_static_easyway_data.run')
    def test_prepare_data(self, prepare_static_easyway_data, mock_print):
        """Provide tests for `prepare_data` custom command."""
        prepare_static_easyway_data.return_value = True
        mock_print.return_value = True

        Command().handle()
        self.assertTrue(prepare_static_easyway_data.called)
        self.assertTrue(mock_print.called)
