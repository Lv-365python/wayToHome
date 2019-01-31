"""This module provides tests of helpers functions for daemons package."""

from argparse import Namespace

from django.test import TestCase
from unittest.mock import patch

from daemons.helper import parse_args


class DaemonHelpersTestCase(TestCase):
    """TestCase for providing daemon`s helper functions testing."""

    @patch('argparse.ArgumentParser.parse_args')
    def test_args_parser(self, mocked_parse_args):
        """Provide tests for the proper parsing of frequency from args."""
        input_frequency = 10

        mocked_parse_args.return_value = Namespace(frequency=input_frequency, minutes=False, hours=False)
        actual_frequency = parse_args()
        self.assertEqual(input_frequency, actual_frequency)

        expected_frequency = input_frequency * 60
        mocked_parse_args.return_value = Namespace(frequency=input_frequency, minutes=True, hours=False)
        actual_frequency = parse_args()
        self.assertEqual(expected_frequency, actual_frequency)

        expected_frequency = input_frequency * 60 * 60
        mocked_parse_args.return_value = Namespace(frequency=input_frequency, minutes=False, hours=True)
        actual_frequency = parse_args()
        self.assertEqual(expected_frequency, actual_frequency)
