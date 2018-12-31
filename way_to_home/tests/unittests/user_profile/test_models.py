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
        custom_user = CustomUser.objects.create(
            id=1,
            email='user@mail.com',
            password='1111',
            is_active=True
        )
        custom_user.save()
        self.user_profile = UserProfile(
            id=2,
            first_name='userName',
            last_name='userSurname',
            user_id=custom_user.id,
        )
        self.user_profile.save()

    def test_str(self):
        """ Test of the __str__() method """
        user_profile = UserProfile.get_by_id(obj_id=self.user_profile.id)
        returned_string = str(user_profile)
        expected_string = f'{user_profile.first_name} {user_profile.last_name}'
        self.assertEqual(returned_string, expected_string)

    def test_to_dict(self):
        """ Test for checking dictionary that 'to_dict' method return"""
        user_profile = UserProfile.get_by_id(obj_id=self.user_profile.id)
        returned_dict = user_profile.to_dict()
        expected_dict = {
            'id': self.user_profile.id,
            'first_name': self.user_profile.first_name,
            'last_name': self.user_profile.last_name,
            'user_id': self.user_profile.user_id
        }
        self.assertDictEqual(returned_dict, expected_dict)
