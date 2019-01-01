"""
CustomUser Model Test
========================
This module provides complete testing for all CustomUser's model functions.
"""

from django.test import TestCase
from custom_user.models import CustomUser


class CustomUserTestCase(TestCase):
    """TestCase for providing CustomUser's model testing"""

    def setUp(self):
        """ Method that provides preparation before testing CustomUser model's features. """
        self.custom_user = CustomUser.objects.create(
            id=1,
            email='user@mail.com',
            google_token={'clientId': '123', 'userKey': 'testuser'},
            phone_number='+380111111111',
            is_active=True
        )
        self.custom_user.set_password('1111')
        self.custom_user.save()

    def test_str(self):
        """ Test of the __str__() method """
        custom_user = CustomUser.objects.get(id=self.custom_user.id)
        returned_string = custom_user.__str__()
        expected_string = f'{self.custom_user.id} {self.custom_user.email}'
        self.assertEqual(returned_string, expected_string)

    def test_to_dict(self):
        """ Test for checking dictionary that 'to_dict' method return """
        custom_user = CustomUser.objects.get(id=self.custom_user.id)
        returned_dict = custom_user.to_dict()
        expected_dict = {
            'id': custom_user.id,
            'email': custom_user.email,
            'phone_number': custom_user.phone_number
        }
        self.assertDictEqual(returned_dict, expected_dict)

    def test_create(self):
        """ Provide tests for 'create' method of certain CustomUser instance """
        custom_user = CustomUser.objects.get(id=self.custom_user.id)
        created_user = CustomUser.create(
            email=custom_user.email,
            password='',
            google_token=custom_user.google_token,
            phone_number=custom_user.phone_number
        )
        # created_user.set_password('2222')

        # self.assertIsInstance(created_user, CustomUser)
        # self.assertIsNotNone(CustomUser.objects.get(id=1))
        #
        # created_user = CustomUser.create(
        #     email=None,
        #     password='',
        #     google_token=custom_user.google_token,
        #     phone_number=custom_user.phone_number
        # )
        self.assertIsNone(created_user)

    def test_get_by_email(self):
        """ Provide tests for 'get_by_email' method of certain CustomUser instance """
        expected_user = CustomUser.objects.get(id=self.custom_user.id)
        returned_user = CustomUser.get_by_email(email=self.custom_user.email)
        self.assertEqual(expected_user, returned_user)

        nonexistent_user = CustomUser.get_by_email(email='some_mail@ukr.net')
        self.assertIsNone(nonexistent_user)
        self.assertRaises(CustomUser.DoesNotExist, CustomUser.objects.get, email='some_mail@ukr.net')

    def test_update(self):
        """Provide tests for 'update' method of certain CustomUser instance."""
        new_password = '2222'
        new_google_token = {'clientId': '222', 'userKey': 'testuser2'}
        new_phone_number = '+380222222222'

        is_updated = self.custom_user.update(
            password=new_password,
            google_token=new_google_token,
            phone_number=new_phone_number
        )
        self.assertTrue(is_updated)

        custom_user = CustomUser.objects.get(id=self.custom_user.id)
        # self.assertEqual(custom_user.password, new_password)
        # self.assertEqual(custom_user.google_token, new_google_token)
        self.assertEqual(custom_user.phone_number, new_phone_number)

        new_phone_number = 0
        is_updated = self.custom_user.update(phone_number=new_phone_number)
        # self.assertFalse(is_updated)
        custom_user = CustomUser.objects.get(id=self.custom_user.id)
        self.assertNotEqual(custom_user.phone_number, new_phone_number)
