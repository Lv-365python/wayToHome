"""
UserProfile Models Test
========================
This module provides complete testing for all UserProfile models functions.
"""

from django.test import TestCase
from custom_user.models import CustomUser
from user_profile.models import UserProfile


class UserProfileModelTestCase(TestCase):
    """ TestCase for providing UserProfile model testing """

    def setUp(self):
        """ Method that provides preparation before testing UserProfile model's features. """
        custom_user = CustomUser.objects.create(
            id=111,
            email='user@mail.com',
            password='1111',
            is_active=True
        )
        custom_user.save()

        CustomUser.objects.create(  # this object use in 'test_create' function
            id=222,
            email='seconduser@mail.com',
            password='2222',
            is_active=True
        ).save()

        self.user_profile = UserProfile.objects.create(
            id=333,
            first_name='userName',
            last_name='userSurname',
            user=custom_user,
            telegram_id=100,
        )
        self.user_profile.save()

    def test_str(self):
        """ Test of the __str__() method """
        user_profile = UserProfile.objects.get(id=self.user_profile.id)
        returned_string = user_profile.__str__()
        expected_string = f'{self.user_profile.first_name} {self.user_profile.last_name}'
        self.assertEqual(returned_string, expected_string)

    def test_to_dict(self):
        """ Test for checking dictionary that 'to_dict' method return """
        user_profile = UserProfile.objects.get(id=self.user_profile.id)
        returned_dict = user_profile.to_dict()
        expected_dict = {
            'id': user_profile.id,
            'first_name': user_profile.first_name,
            'last_name': user_profile.last_name,
            'user_id': user_profile.user_id,
            'telegram_id': 100
        }
        self.assertDictEqual(returned_dict, expected_dict)

    def test_create(self):
        """ Provide tests for 'create' method of certain UserProfile instance """
        custom_user = CustomUser.objects.get(id=222)
        created_user_profile = UserProfile.create(
            user=custom_user,
            first_name='userName',
            last_name='userSurname',
        )

        self.assertIsInstance(created_user_profile, UserProfile)
        self.assertIsNotNone(UserProfile.objects.get(id=created_user_profile.id))

        created_user_profile = UserProfile.create(
            user=None,
            first_name='userName',
            last_name='userSurname',
        )
        self.assertIsNone(created_user_profile)

    def test_get_by_id(self):
        """ Provide tests for 'get_by_id' method of certain UserProfile instance """
        expected_user_profile = UserProfile.objects.get(id=self.user_profile.id)
        returned_user_profile = UserProfile.get_by_id(obj_id=self.user_profile.id)
        self.assertEqual(expected_user_profile, returned_user_profile)

        nonexistent_user = UserProfile.get_by_id(obj_id=100)
        self.assertIsNone(nonexistent_user)
        self.assertRaises(UserProfile.DoesNotExist, UserProfile.objects.get, id=100)

    def test_delete_by_id(self):
        """Provide tests for 'delete_by_id' method of certain UserProfile instance."""
        is_deleted = UserProfile.delete_by_id(obj_id=self.user_profile.id)
        self.assertTrue(is_deleted)
        self.assertRaises(UserProfile.DoesNotExist, UserProfile.objects.get, id=self.user_profile.id)

        is_deleted = UserProfile.delete_by_id(obj_id=100)
        self.assertFalse(is_deleted)

    def test_update(self):
        """Provide tests for 'update' method of certain UserProfile instance."""
        new_first_name = 'new_userName'
        new_last_name = 'new_userSurname'
        is_updated = self.user_profile.update(first_name=new_first_name, last_name=new_last_name)
        self.assertTrue(is_updated)

        user_profile = UserProfile.objects.get(id=self.user_profile.id)
        self.assertEqual(user_profile.first_name, new_first_name)
        self.assertEqual(user_profile.last_name, new_last_name)

        is_updated = self.user_profile.update(first_name=new_first_name,
                                              last_name=new_last_name,
                                              telegram_id='wrong_id',
                                              )
        self.assertFalse(is_updated)

    def test_get_by_telegram_id(self):
        """ Provide tests for 'get_by_telegram_id' method of certain UserProfile instance """
        expected_user_profile = UserProfile.objects.get(telegram_id=self.user_profile.telegram_id)
        returned_user_profile = UserProfile.get_by_telegram_id(telegram_id=self.user_profile.telegram_id)
        self.assertEqual(expected_user_profile, returned_user_profile)

        nonexistent_user_profile = UserProfile.get_by_telegram_id(telegram_id='wrong_id')
        self.assertIsNone(nonexistent_user_profile)

        nonexistent_user_profile = UserProfile.get_by_telegram_id(telegram_id=200)
        self.assertIsNone(nonexistent_user_profile)
