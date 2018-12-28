"""
CustomUser view tests
========================
This module provides complete testing for all CustomUser's views functions.
"""

from django.urls import reverse
from django.test import TestCase, Client
from custom_user.models import CustomUser


class CustomProfileViewTest(TestCase):
    """TestCase for providing CustomUser's view testing."""
