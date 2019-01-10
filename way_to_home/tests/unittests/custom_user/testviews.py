"""
CustomUser view tests
========================
This module provides complete testing for all CustomUser's views functions.
"""

import json
from django.urls import reverse
from django.test import TestCase, Client
from custom_user.models import CustomUser
from utils.jwttoken import create_token
from unittest import mock


class CustomUserViewTest(TestCase):
    """TestCase for providing CustomUser's view testing."""

    def setUp(self):
        """ Method that provides preparation before testing CustomUser views."""
        self.custom_user = CustomUser.objects.create(
            id=1001,
            email='user@mail.com',
            phone_number='+380111111111',
            is_active=True
        )
        self.custom_user.set_password('1111Bb')
        self.custom_user.save()

        self.inactive_user = CustomUser.objects.create(
            id=1111,
            email='user22@mail.com',
            phone_number='+380111111111',
        )
        self.inactive_user.set_password('2222Bb')
        self.inactive_user.save()

        self.client = Client()

    def test_sign_up(self):
        """Provides test for a (POST) request to sign up a user with correct signup data."""
        data = {
            'email': 'another@mail.com',
            'password': '123456789aA'
        }
        url = reverse('signup')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_sign_up_already_exists(self):
        """Provides test for a (POST) request to sign up a user with taken email in request body."""
        test_data = {
            'email': 'user@mail.com',
            'password': '123456789aA'
        }
        url = reverse('signup')
        response = self.client.post(url, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_sign_up_failed_email(self):
        """Provides test for a (POST) request to sign up a user with inappropriate email in request body."""
        test_data = {
            'email': 'user',
            'password': '123456789aA'
        }
        url = reverse('signup')
        response = self.client.post(url, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_sign_up_failed_password(self):
        """Provides test for a (POST) request to sign up a user with inappropriate password in request body."""
        test_data = {
            'email': 'another@mail.com',
            'password': '123'
        }
        url = reverse('signup')
        response = self.client.post(url, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_confirm(self):
        """Provides test for a (GET) request to confirm user sign up with correct token."""
        token = create_token(data={'email': self.inactive_user.email})
        url = reverse('confirm_signup', kwargs={'token': token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_signup_confirm_invalid_token(self):
        """Provides test for a (GET) request to confirm user sign up with incorrect token."""
        token = 'bad_token'
        url = reverse('confirm_signup', kwargs={'token': token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 498)

    def test_signup_confirm_invalid_email(self):
        """Provides test for a (GET) request to confirm user sign up with token for an email that wasn't registered."""
        token = create_token(data={'email': 'random@email'})
        url = reverse('confirm_signup', kwargs={'token': token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)

    def test_signup_db_error(self):
        token = create_token(data={'email': self.inactive_user.email})
        url = reverse('confirm_signup', kwargs={'token': token})

        with mock.patch('custom_user.models.CustomUser.update') as update:
            update.return_value = False
            response = self.client.get(url)

        self.assertEqual(response.status_code, 400)

    def test_log_in(self):
        """Provides test for a (POST) request to log in a registered user with correct credentials."""
        test_data = {
            'email': 'user@mail.com',
            'password': '1111Bb'
        }
        url = reverse('login_user')
        response = self.client.post(url, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_log_in_fail(self):
        """Provides test for a (POST) request to log in a registered user with incorrect credentials."""
        test_data = {
            'email': 'wrong_email@mail.com',
            'password': 'Randompassword123'
        }
        url = reverse('login_user')
        response = self.client.post(url, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_log_in_validator_fail(self):
        test_data = {
            'email': 'not_valid_email',
            'password': 'not_valid_password'
        }
        url = reverse('login_user')
        response = self.client.post(url, json.dumps(test_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_google_auth_success(self):
        """Provides test for a (GET) request to authenticate via Google."""
        url = reverse('auth_google')
        expected_reverse = reverse('sign_in_google')
        with mock.patch('requests_oauthlib.OAuth2Session.authorization_url') as authorization_url:
            authorization_url.return_value = [expected_reverse]
            response = self.client.get(url, follow=True)
            self.assertEquals(response.redirect_chain[0], (expected_reverse, 302))

    def test_google_auth_fail(self):
        """Provides test for a (GET) request to authenticate via Google."""
        url = reverse('auth_google')
        with mock.patch('requests_oauthlib.OAuth2Session.authorization_url') as authorization_url:
            authorization_url.return_value = ['']
            response = self.client.get(url, follow=True)
            self.assertEquals(response.status_code, 403)
