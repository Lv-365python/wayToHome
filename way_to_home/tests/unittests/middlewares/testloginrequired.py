"""This module provides tests for custom LoginRequired middleware."""

from django.test import TestCase, Client

from custom_user.models import CustomUser
from middlewares.login_required import GUESTS_PATHS


class LoginRequiredTestCase(TestCase):
    """TestCase for providing LoginRequired middleware testing."""

    def setUp(self):
        """Provide preparation before testing middleware."""
        user = CustomUser(id=100, email='testuser@mail.com', is_active=True)
        user.set_password('testpassword')
        user.save()

        self.guest_client = Client()

        self.user_client = Client()
        self.user_client.login(email='testuser@mail.com', password='testpassword')

    def test_post_with_invalid_json(self):
        """Provide tests for POST request with invalid JSON data."""
        path = '/api/'
        invalid_json = 'invalid json'

        response = self.client.post(path, invalid_json, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_put_with_invalid_json(self):
        """Provide tests for PUT request with invalid JSON data."""
        path = '/api/'
        invalid_json = 'invalid json'

        response = self.client.put(path, invalid_json, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_forbidden_request_for_user(self):
        """Provide tests for user`s GET requests with paths that available only for guests."""
        for path in GUESTS_PATHS:
            response = self.user_client.get(path)
            self.assertEqual(response.status_code, 403)

    def test_forbidden_request_for_guest(self):
        """Provide tests for guest`s requests with path that available only for users."""
        path = '/api/'

        response = self.guest_client.get(path)
        self.assertEqual(response.status_code, 403)
