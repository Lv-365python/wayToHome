"""
UserProfile view tests
========================
This module provides complete testing for all CustomUser's views functions.
"""

from django.test import TestCase, Client
from unittest import mock
from custom_user.models import CustomUser
from user_profile.models import UserProfile
from django.urls import reverse
import json


class UserProfileViewTest(TestCase):
    """Test Case that provides testing of User Profile view"""
    def setUp(self):
        """Method that provides preparation before testing User Profile view`s features."""
        self.url = reverse('profile')

        self.first_user = CustomUser.objects.create(
            id=1001,
            email='user@mail.com',
            phone_number='+380111111111',
            is_active=True
        )
        self.first_user.set_password('1111Bb')
        self.first_user.save()

        self.user_profile = UserProfile.objects.create(
            id=1111,
            user=self.first_user,
            first_name='Jhon',
            last_name='Doe'
        )

        self.second_user = CustomUser.objects.create(
            id=2002,
            email='user2@mail.com',
            phone_number='+380111111112',
        )
        self.second_user.set_password('2222Bb')
        self.second_user.save()

        self.client = Client()
        self.client.login(email='user@mail.com', password='1111Bb')

        self.second_client = Client()
        self.second_client.login(email='user2@mail.com', password='2222Bb')

    def test_get(self):
        """Method that tests the successful request to retrieve user_profile"""
        expected_response = {
            'id': 1111,
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'user_id': 1001,
            'telegram_id': None
        }

        response = self.client.get(self.url)
        self.assertJSONEqual(json.dumps(expected_response), json.loads(response.content))
        self.assertEqual(response.status_code, 200)

    def test_get_fail(self):
        """Method that tests the unsuccessful request to retrieve user_profile"""
        response = self.second_client.get(self.url)
        self.assertEquals(response.status_code, 400)

    def test_put_success(self):
        """Method that tests the successful request to update user_profile"""
        test_data = {
            'first_name': 'new_first_name',
            'last_name': 'new_last_name'
        }
        response = self.client.put(self.url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 200)

    def test_put_no_profile(self):
        """Method that tests the unsuccessful request to update user_profile in case when profile is not found"""
        test_data = {
            'first_name': 'new_first_name',
            'last_name': 'new_last_name'
        }
        response = self.second_client.put(self.url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_put_no_data(self):
        """Method that tests the unsuccessful request to update user_profile in case when new data is not provided"""
        test_data = {}
        response = self.client.put(self.url, json.dumps(test_data), content_type='application/json')
        self.assertEquals(response.status_code, 400)

    def test_put_db_fail(self):
        """Method that tests the unsuccessful request to update user_profile in case of database failure"""
        test_data = {
            'first_name': 'new_first_name',
            'last_name': 'new_last_name'
        }
        with mock.patch('utils.abstract_models.AbstractModel.update') as update:
            update.return_value = False
            response = self.client.put(self.url, json.dumps(test_data), content_type='application/json')
            self.assertEquals(response.status_code, 400)

    def test_put_validation_fail(self):
        """Method that tests the unsuccessful request to update user_profile in case of data not passing validation"""
        test_data = {
            'first_name': 'new_first_name',
            'last_name': 'new_last_name'
        }

        with mock.patch('user_profile.views.profile_validator') as profile_validator:
            profile_validator.return_value = False
            response = self.client.put(self.url, json.dumps(test_data), content_type='application/json')
            self.assertEquals(response.status_code, 400)
