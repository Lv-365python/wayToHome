"""
UserProfile Models Test
========================
This module provides complete testing for all UserProfile models functions.
"""

from django.test import TestCase
from custom_user.models import CustomUser
from user_profile.models import UserProfile


class UserProfileTestCase(TestCase):
    """ TestCase for providing UserProfile model testing """

    def setUp(self):
        """ Method that provides preparation before testing UserProfile model's features. """
        user = CustomUser.objects.create(id=1, email='user@mail.com', password='1111', is_active=True)
        first_name = CustomUser.objects.create('userName')
        last_name = CustomUser.objects.create('userSurname')

    def test_str(self):
        """ Test of the __str__() method """
        returned_string = str(CustomUser.objects.get(id=1))
        expected_string = 'userName userSurname'
        self.assertEqual(returned_string, expected_string)
