"""This module provides tests for custom LoginRequired middleware."""

from django.test import TestCase, Client
from django.urls import reverse

from custom_user.models import CustomUser
from middlewares.login_required import GUESTS_PATHS


class LoginRequiredTestCase(TestCase):
    """TestCase for providing LoginRequired middleware testing."""

    def setUp(self):
        """Provide preparation before testing middleware."""
        user = CustomUser(id=100, email='testuser@mail.com', is_active=True)
        user.set_password('Testpassword123')
        user.save()

        self.guest_client = Client()

        self.user_client = Client()
        self.user_client.login(email='testuser@mail.com', password='Testpassword123')

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
        """Provide tests for user`s GET requests with paths that are available only for guests."""
        for path in GUESTS_PATHS:
            response = self.user_client.get(path)
            self.assertEqual(response.status_code, 403)

    def test_forbidden_request_for_guest(self):
        """Provide tests for guest`s requests with path that is available only for users."""
        path = '/api/'

        response = self.guest_client.get(path)
        self.assertEqual(response.status_code, 403)

    def test_success_request_for_guest(self):
        """Provide tests for success guest`s request."""
        path = reverse('login_user')
        credentials = {
            'email': 'testuser@mail.com',
            'password': 'Testpassword123'
        }

        response = self.guest_client.post(path, credentials, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_success_request_for_user(self):
        """Provide tests for success user`s request."""
        path = reverse('place')

        response = self.user_client.get(path)
        self.assertEqual(response.status_code, 200)

    def test_success_request_for_home(self):
        """Provide tests for success requests on `home` URL both for user and guest."""
        path = reverse('index')

        response = self.guest_client.get(path)
        self.assertEqual(response.status_code, 200)

        response = self.user_client.get(path)
        self.assertEqual(response.status_code, 200)
