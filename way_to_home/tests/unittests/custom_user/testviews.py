"""
CustomUser view tests
========================
This module provides complete testing for all CustomUser's views functions.
"""

import json

from django.db import DatabaseError
from django.urls import reverse
from django.test import TestCase, Client
from custom_user.models import CustomUser
from utils.jwttoken import create_token
from unittest import mock


class MockObjectGetNew:
    """
    Class of mock object to use in place of
    get attribute of google Oauth session,
    if attribute json is called, it returns new email
    """
    def json(self, *args, **kwargs):
        """mock for google session .get.json(), returns new email"""
        return {'email': 'test_mail@mail.com'}


class MockObjectGetExisting:
    """
    Class of mock object to use in place of
    get attribute of google Oauth session,
    if attribute json is called, it returns registered email
    """
    def json(self, *args, **kwargs):
        """mock for google session .get.json(), returns existing email"""
        return {'email': 'user@mail.com'}


class MockObjectGetEmpty:
    """
    Class of mock object to use in place of
    get attribute of google Oauth session,
    if attribute json is called, it returns empty json
    """
    def json(self, *args, **kwargs):
        """mock for google session .get.json(), returns empty json"""
        return {}


class GoogleMock:
    """Class of mock object to use in place of google Oauth session"""
    def fetch_token(self, *args, **kwargs):
        """mock that replaces fetch_token attribute of google oauth session"""
        pass

    def get_new(self, *args, **kwargs):
        """mock to replace get attribute of google oauth session, in case we need to receive new email"""
        mock_get = MockObjectGetNew()
        return mock_get

    def get_existing(self, *args, **kwargs):
        """mock to replace get attribute of google oauth session, in case we need to receive existing email"""
        mock_get = MockObjectGetExisting()
        return mock_get

    def get_empty(self, *args, **kwargs):
        """mock to replace get attribute of google oauth session, in case we need to receive empty json"""
        mock_get = MockObjectGetEmpty()
        return mock_get


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

    def test_signup_db_update_error(self):
        token = create_token(data={'email': self.inactive_user.email})
        url = reverse('confirm_signup', kwargs={'token': token})

        with mock.patch('custom_user.models.CustomUser.update') as update:
            update.side_effect = DatabaseError()
            response = self.client.get(url)

        self.assertEqual(response.status_code, 400)

    def test_signup_db_create_error(self):
        token = create_token(data={'email': self.inactive_user.email})
        url = reverse('confirm_signup', kwargs={'token': token})

        with mock.patch('user_profile.models.UserProfile.create') as create:
            create.side_effect = DatabaseError()
            response = self.client.get(url)

        self.assertEqual(response.status_code, 400)

    def test_log_in(self):
        """Provides test for a (POST) request to log in a registered user with correct credentials."""
        test_data = {
            'email': 'user@mail.com',
            'password': '1111Bb',
            'save_cookies': True,
        }
        url = reverse('login_user')
        response = self.client.post(url, json.dumps(test_data), content_type='application/json')
        self.assertIn('user_id', response.cookies)
        self.assertNotEqual(response.cookies['user_id'].value, '')
        self.assertEqual(response.status_code, 200)

    def test_log_in_fail(self):
        """Provides test for a (POST) request to log in a registered user with incorrect credentials."""
        test_data = {
            'email': 'wrong_email@mail.com',
            'password': 'Randompassword123',
            'save_cookies': True,
        }
        url = reverse('login_user')
        response = self.client.post(url, json.dumps(test_data), content_type='application/json')
        self.assertNotIn('user_id', response.cookies)
        self.assertEqual(response.status_code, 400)

    def test_log_in_validator_fail(self):
        """Provides test for a (POST) request to log in a registered user with credentials that don't pass validator."""
        test_data = {
            'email': 'not_valid_email',
            'password': 'not_valid_password',
            'save_cookies': True,
        }
        url = reverse('login_user')
        response = self.client.post(url, json.dumps(test_data), content_type='application/json')
        self.assertNotIn('user_id', response.cookies)
        self.assertEqual(response.status_code, 400)

    def test_logout(self):
        """ Positive user logout test """
        test_data = {
            'email': 'user@mail.com',
            'password': '1111Bb',
        }
        response = self.client.login(**test_data)
        self.assertEqual(response, True)

        url_logout = reverse('logout_user')
        resp_logout = self.client.get(url_logout)
        self.assertEqual(resp_logout.cookies['user_id'].value, '')
        self.assertEqual(resp_logout.status_code, 200)

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

    def test_delete_account_success(self):
        """Method that tests successful deleting user account"""
        self.client.login(username='user@mail.com', password='1111Bb')
        url = reverse('delete_account')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)

    def test_delete_account_fail(self):
        """Method that tests failing deleting user account"""
        self.client.login(username='user@mail.com', password='1111Bb')
        url = reverse('delete_account')
        with mock.patch('custom_user.models.CustomUser.delete_by_id') as is_deleted:
            is_deleted.return_value = False
            response = self.client.delete(url)
        self.assertEqual(response.status_code, 400)

    @mock.patch('requests_oauthlib.OAuth2Session.fetch_token', GoogleMock.fetch_token)
    @mock.patch('requests_oauthlib.OAuth2Session.get', GoogleMock.get_new)
    def test_google_signup_success(self):
        """Provides test for a (GET) request to authenticate via Google creating new user."""
        url = reverse('sign_in_google')
        code = 'test_code'
        uri = f'{url}?code={code}'
        response = self.client.get(uri)
        self.assertEquals(response.status_code, 201)

    @mock.patch('requests_oauthlib.OAuth2Session.fetch_token', GoogleMock.fetch_token)
    @mock.patch('requests_oauthlib.OAuth2Session.get', GoogleMock.get_existing)
    def test_google_login_success(self):
        """Provides test for a (GET) request to authenticate via Google and log in existing user."""
        url = reverse('sign_in_google')
        code = 'test_code'
        uri = f'{url}?code={code}'
        response = self.client.get(uri)
        self.assertEquals(response.status_code, 200)

    @mock.patch('requests_oauthlib.OAuth2Session.fetch_token', GoogleMock.fetch_token)
    @mock.patch('requests_oauthlib.OAuth2Session.get', GoogleMock.get_empty)
    def test_google_empty_json(self):
        """Provides test for a (GET) request to authenticate via Google in case of no user_data received from google"""
        url = reverse('sign_in_google')
        code = 'test_code'
        uri = f'{url}?code={code}'
        response = self.client.get(uri)
        self.assertEquals(response.status_code, 400)

    def test_reset_password_success(self):
        """Provides test for a (POST) request to reset password for not authenticated user in case of success"""
        url = reverse('reset_password')
        test_data = {'email': self.custom_user.email}
        response = self.client.post(url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 200)

    def test_reset_password_validation_fail(self):
        """Provides test for a (POST) request to reset password in case of email not passing email validation"""
        url = reverse('reset_password')
        test_data = {'email': 'not_email'}
        response = self.client.post(url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_reset_password_no_such_user(self):
        """Provides test for a (POST) request to reset password in case of receiving email of non-existent user"""
        url = reverse('reset_password')
        test_data = {'email': 'not_a_user@mail.com'}
        response = self.client.post(url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_confirm_reset_password_success(self):
        """Provides test for a (PUT) request to confirm reset password in case of success"""
        token = create_token(data={'email': self.custom_user.email})
        url = reverse('confirm_reset_password', kwargs={'token': token})
        test_data = {'new_password': '1234Bbcd'}
        response = self.client.put(url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 200)

    def test_confirm_reset_password_invalid_token(self):
        """Provides test for a (PUT) request to confirm reset of password in case of receiving faulty token"""
        token = ' '
        url = reverse('confirm_reset_password', kwargs={'token': token})
        test_data = {'new_password': '1234Bbcd'}
        response = self.client.put(url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 498)

    def test_confirm_reset_password_no_such_user(self):
        """Provides test for a (PUT) request to confirm reset of password in case of receiving faulty token"""
        token = create_token(data={'email': 'not_a_user@mail.com'})
        url = reverse('confirm_reset_password', kwargs={'token': token})
        test_data = {'new_password': '1234Bbcd'}
        response = self.client.put(url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_confirm_reset_password_validation_fail(self):
        """Provides test for a (PUT) request to confirm reset of password in case of receiving faulty token"""
        token = create_token(data={'email': self.custom_user.email})
        url = reverse('confirm_reset_password', kwargs={'token': token})
        test_data = {'new_password': 'bad'}
        response = self.client.put(url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_confirm_reset_password_same_password(self):
        """Provides test for a (PUT) request to confirm reset of password in case of receiving old password"""
        token = create_token(data={'email': self.custom_user.email})
        url = reverse('confirm_reset_password', kwargs={'token': token})
        test_data = {'new_password': self.custom_user.password}
        response = self.client.put(url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_confirm_reset_password_db_fail(self):
        """Provides test for a (PUT) request to confirm reset of password in case of database failure"""
        token = create_token(data={'email': self.custom_user.email})
        url = reverse('confirm_reset_password', kwargs={'token': token})
        test_data = {'new_password': '1234Bbcd'}
        with mock.patch('custom_user.models.CustomUser.update') as update:
            update.return_value = False
            response = self.client.put(url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_change_password_success(self):
        """Provides test for a (PUT) request to change password in case of success"""
        self.client.login(email='user@mail.com', password='1111Bb')
        url = reverse('change_password')
        test_data = {
            'new_password': '1234Bbcd',
            'old_password': '1111Bb'
        }
        response = self.client.put(url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 200)

    def test_change_password_wrong_old_password(self):
        """Provides test for a (PUT) request to change password in case of old password being wrong"""
        self.client.login(email='user@mail.com', password='1111Bb')
        url = reverse('change_password')
        test_data = {
            'new_password': '1111Bb',
            'old_password': 'Wrong_old_pass123'
        }
        response = self.client.put(url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_change_password_to_invalide(self):
        """Provides test for a (PUT) request to change password in case of new password being invalid"""
        self.client.login(email='user@mail.com', password='1111Bb')
        url = reverse('change_password')
        test_data = {
            'new_password': '1',
            'old_password': '1111Bb'
        }
        response = self.client.put(url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_change_password_to_old(self):
        """Provides test for a (PUT) request to change password in case of attempt to change password to old password"""
        self.client.login(email='user@mail.com', password='1111Bb')
        url = reverse('change_password')
        test_data = {
            'new_password': '1111Bb',
            'old_password': '1111Bb'
        }
        response = self.client.put(url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_change_password_db_fail(self):
        """Provides test for a (PUT) request to change password in case of database error"""
        self.client.login(email='user@mail.com', password='1111Bb')
        url = reverse('change_password')
        test_data = {
            'new_password': '1234Bbcd',
            'old_password': '1111Bb'
        }
        with mock.patch('custom_user.models.CustomUser.update') as update:
            update.return_value = False
            response = self.client.put(url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 400)
