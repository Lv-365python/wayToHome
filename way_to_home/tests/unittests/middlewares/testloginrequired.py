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
        user.set_password('testpassword')
        user.save()

        self.guest_client = Client()

        self.user_client = Client()
        self.user_client.login(email='testuser@mail.com', password='testpassword')

    def test_invalid_json(self):
        """Provide tests for PUT/POST/PATCH request with invalid JSON data."""
        data = 'invalid data'

        response = self.client.post('/api/', data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.client.put('/api/', data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        response = self.client.patch('/api/', data, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_forbidden_request_for_user(self):
        """Provide tests guests path for authenticated user."""
        data = {}
        for path in GUESTS_PATHS:
            response = self.user_client.get(path)
            self.assertEqual(response.status_code, 403)

            response = self.user_client.post(path, data, content_type='application/json')
            self.assertEqual(response.status_code, 403)

            response = self.user_client.put(path, data, content_type='application/json')
            self.assertEqual(response.status_code, 403)

            response = self.user_client.patch(path, data, content_type='application/json')
            self.assertEqual(response.status_code, 403)

    def test_forbidden_request_for_guest(self):
        """Provide tests unsuccessful requests for guest."""
        path = reverse('place')
        data = {}

        response = self.guest_client.get(path)
        self.assertEqual(response.status_code, 403)

        response = self.guest_client.post(path, data, content_type='application/json')
        self.assertEqual(response.status_code, 403)

        response = self.guest_client.put(path, data, content_type='application/json')
        self.assertEqual(response.status_code, 403)

        response = self.guest_client.patch(path, data, content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_success_request_for_guest(self):
        """Provide tests successful requests for guest."""
        path = reverse('login_user')
        credentials = {'email': 'testuser@mail.com', 'password': 'testpassword'}

        response = self.guest_client.post(path, credentials, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_success_request_for_user(self):
        """Provide tests successful requests for authenticated user."""
        path = reverse('place')

        response = self.user_client.get(path)
        self.assertEqual(response.status_code, 200)
