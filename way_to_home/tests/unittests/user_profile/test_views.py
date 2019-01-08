"""
UserProfile view tests
========================
This module provides complete testing for all CustomUser's views functions.
"""

from django.test import TestCase, Client
from custom_user.models import CustomUser
from user_profile.models import UserProfile
from django.urls import reverse


class UserProfileViewTest(TestCase):
    """Test Case that provides testing of User Profile view"""
    def setUp(self):
        self.custom_user = CustomUser.objects.create(
            id=1001,
            email='user@mail.com',
            phone_number='+380111111111',
            is_active=True
        )
        self.custom_user.set_password('1111Bb')
        self.custom_user.save()

        self.user_profile = UserProfile.objects.create(
            id=1111,
            user=self.custom_user,
            first_name='Jhon',
            last_name='Doe'
        )

        self.second_user = CustomUser.objects.create(
            id=2002,
            email='user2@mail.com',
            phone_number='+380111111112',
            is_active=True
        )
        self.second_user.set_password('2222Bb')
        self.second_user.save()

        self.client = Client()
        self.client.login(email=self.custom_user.email, password=self.custom_user.password)

    def test_get_id(self):
        expected_response = {
            'id': 1111,
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'user_id': 1001
        }
        url = reverse('profile', kwargs={'profile_id': '1001'})

        response = self.client.get(url)
        self.assertJSONEqual(expected_response, response.body)
        self.assertEqual(response.status_code, 200)

        response = self.client.get(url_no_id)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(url_id)
        self.assertEqual(response.status_code, 403)


    def test_without_id(self):
        expected_response = {
            'id': 1111,
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'user_id': 1001
        }
        url = reverse('profile')
        response = self.client.get(url)
        self.assertJSONEqual(expected_response, response.body)
        self.assertEqual(response.status_code, 200)


    def test_non_existent(self):
        url = reverse('profile', kwargs={'profile_id': '9999'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_profileless_user(self):
        self.client.login(email=self.second_user.email, password=self.second_user.password)
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual()
