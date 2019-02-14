"""This module provides tests for JWT helpers functions."""

import jwt
from django.test import TestCase
from django.utils import timezone
from utils.jwthelper import decode_token, create_token, SECRET_KEY, ALGORITHM


class JWTHelperTestCase(TestCase):
    """TestCase for providing 'jwthelper' util testing."""

    def test_create_token_success(self):
        """Method that tests succeeded `create_token` method."""
        test_data = {'email': 'user@gmail.com'}
        expected_token = jwt.encode(test_data, SECRET_KEY, ALGORITHM).decode("utf-8")
        returned_token = create_token(test_data)
        self.assertEquals(returned_token, expected_token)

    def test_create_token_error(self):
        """Method that tests unsucceeded `create_token` method."""
        wrong_data = 'email'
        returned_token = create_token(wrong_data)
        self.assertIsNone(returned_token)

    def test_create_token_success_expiration_time(self):
        """Method that tests succeeded `create_token` method with expiration time parameter."""
        expiration_time = 60
        test_data = {'email': 'user@gmail.com'}
        test_data_exp = {'email': 'user@gmail.com', 'exp': int(timezone.now().timestamp()) + expiration_time}
        expected_token = jwt.encode(test_data_exp, SECRET_KEY, ALGORITHM).decode("utf-8")
        returned_token = create_token(test_data, expiration_time=expiration_time)
        self.assertEquals(returned_token, expected_token)

    def test_create_token_success_not_before_time(self):
        """Method that tests succeeded `create_token` method with not before time parameter."""
        time_before = 120
        test_data = {'email': 'user@gmail.com'}
        test_data_before = {'email': 'user@gmail.com', 'nbf': int(timezone.now().timestamp()) + time_before}
        expected_token = jwt.encode(test_data_before, SECRET_KEY, ALGORITHM).decode("utf-8")
        returned_token = create_token(test_data, time_before=time_before)
        self.assertEquals(returned_token, expected_token)

    def test_decode_token_success(self):
        """Method that tests succeeded `decode_token` method."""
        test_data = {'email': 'user@gmail.com'}
        token = jwt.encode(test_data, SECRET_KEY, ALGORITHM)
        expected_dict = {'email': 'user@gmail.com'}
        returned_dict = decode_token(token)
        self.assertDictEqual(returned_dict, expected_dict)

    def test_decode_token_fail_none(self):
        """Method that tests unsucceeded `decode_token` method."""
        test_data = {'email': 'user@gmail.com', 'exp': 100500}
        token = jwt.encode(test_data, SECRET_KEY, ALGORITHM)
        returned_dict = decode_token(token)
        self.assertIsNone(returned_dict)
