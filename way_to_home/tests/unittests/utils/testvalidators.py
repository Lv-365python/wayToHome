"""
Validators Test
========================
This module provides complete testing for all validators.
"""

from django.test import TestCase
from utils.validators import (string_validator, coordinate_validator, required_keys_validator,
                              none_validator_for_required_keys, date_validator, start_date_validator,
                              end_date_validator, time_validator, week_day_validator, email_validator,
                              password_validator, credentials_validator, profile_validator, phone_validator,
                              notification_data_validator, place_data_validator, route_data_validator,
                              way_data_validator)


class ValidatorsTestCase(TestCase):
    """Test Case that provides testing of validators"""
    def test_string_validator(self):
        """Method that tests the string_validator function"""
        not_str_value = 123
        result = string_validator(value=not_str_value)
        self.assertFalse(result)

        invalid_data = {'value': 'test',
                        'min_length': 5}
        result = string_validator(**invalid_data)
        self.assertFalse(result)

        invalid_data = {'value': 'test',
                        'max_length': 2}
        result = string_validator(**invalid_data)
        self.assertFalse(result)

        valid_value = 'test'
        result = string_validator(value=valid_value)
        self.assertTrue(result)

        test_data = {'value': 'test',
                     'min_length': 2,
                     'max_length': 5}
        result = string_validator(**test_data)
        self.assertTrue(result)

    def test_coordinate_validator(self):
        """Method that tests the coordinate_validator function"""
        invalid_data = {'value': 'test',
                        'min_value': -180,
                        'max_value': 180}
        result = coordinate_validator(**invalid_data)
        self.assertFalse(result)

        invalid_data = {'value': 360.0,
                        'min_value': -180,
                        'max_value': 180}
        result = coordinate_validator(**invalid_data)
        self.assertFalse(result)

        invalid_data = {'value': -360.0,
                        'min_value': -180,
                        'max_value': 180}
        result = coordinate_validator(**invalid_data)
        self.assertFalse(result)

        test_data = {'value': 42.1241,
                     'min_value': -180,
                     'max_value': 180}
        result = coordinate_validator(**test_data)
        self.assertTrue(result)

    def test_required_keys_validator(self):
        """Method that tests the required_keys_validator function"""
        invalid_data = {'key1': 'test',
                        'key2': 'test'}
        test_required_keys = ['key1', 'key2', 'key3']
        result = required_keys_validator(data=invalid_data, keys_required=test_required_keys)
        self.assertFalse(result)

        test_data = {'key1': 'test',
                     'key2': 'test',
                     'key3': 'test'}
        test_required_keys = ['key1', 'key2', 'key3']
        result = required_keys_validator(data=test_data, keys_required=test_required_keys)
        self.assertTrue(result)

    def test_none_validator_for_required_keys(self):
        """Method that tests the none_validator_for_required_keys function"""
        invalid_data = {'key1': None,
                        'key2': None}
        test_required_keys = ['key1', 'key2']
        result = none_validator_for_required_keys(data=invalid_data, keys_required=test_required_keys)
        self.assertFalse(result)

        test_data = {'key1': 'test',
                     'key2': 'test'}
        test_required_keys = ['key1', 'key2']
        result = none_validator_for_required_keys(data=test_data, keys_required=test_required_keys)
        self.assertTrue(result)

    def test_date_validator(self):
        """Method that tests the date_validator function"""
        invalid_date = 123
        result = date_validator(date=invalid_date)
        self.assertIsNone(result)

        invalid_date = '12323fd'
        result = date_validator(date=invalid_date)
        self.assertIsNone(result)

        test_date = ['20190212', '2019-02-12', '12-02-2019', '12022019', '02122019', '12/02/2019']

        for date in test_date:
            result = date_validator(date=date)
            self.assertNotEqual(result, None)

    def test_start_date_validator(self):
        """Method that tests the start_date_validator function"""
        invalid_date = 123
        result = start_date_validator(start_date=invalid_date)
        self.assertFalse(result)

        invalid_date = '12323fd'
        result = start_date_validator(start_date=invalid_date)
        self.assertFalse(result)

        test_date = ['20190212', '2019-02-12', '12-02-2019', '12022019', '02122019', '12/02/2019']

        for date in test_date:
            result = start_date_validator(start_date=date)
            self.assertTrue(result)

    def test_end_date_validator(self):
        """Method that tests the end_date_validator function"""
        invalid_date = {'end_date': 123,
                        'start_date': '2019-02-12'}
        result = end_date_validator(**invalid_date)
        self.assertFalse(result)

        invalid_date = {'end_date': '2019-01-12',
                        'start_date': '2019-02-12'}
        result = end_date_validator(**invalid_date)
        self.assertFalse(result)

        test_date = {'end_date': '2019-02-12',
                     'start_date': '2019-01-12'}
        result = end_date_validator(**test_date)
        self.assertTrue(result)

    def test_time_validator(self):
        """Method that tests the time_validator function"""
        invalid_time = 123
        result = time_validator(time=invalid_time)
        self.assertFalse(result)

        invalid_time = '12323fd'
        result = time_validator(time=invalid_time)
        self.assertFalse(result)

        invalid_time = '25:61:61'
        result = time_validator(time=invalid_time)
        self.assertFalse(result)

        test_time = '21:43:23'
        result = time_validator(time=test_time)
        self.assertTrue(result)

    def test_week_day_validator(self):
        """Method that tests the week_day_validator function"""
        invalid_week_day = 'fgs'
        result = week_day_validator(week_day=invalid_week_day)
        self.assertFalse(result)

        invalid_week_day = 7
        result = week_day_validator(week_day=invalid_week_day)
        self.assertFalse(result)

        invalid_week_day = -1
        result = week_day_validator(week_day=invalid_week_day)
        self.assertFalse(result)

        for day in range(0, 7):
            result = week_day_validator(week_day=day)
            self.assertTrue(result)

    def test_notification_data_validator(self):
        """Method that tests the notification_data_validator function"""
        invalid_data = {'start_time': '2019-01-12',
                        'end_time': '2019-02-12'}
        result = notification_data_validator(data=invalid_data)
        self.assertFalse(result)

        invalid_data = {'start_time': '2019-01-12',
                        'end_time': '2019-02-12',
                        'week_day': 2,
                        'time': None}
        result = notification_data_validator(data=invalid_data)
        self.assertFalse(result)

        invalid_data = {'start_time': 'invalid time',
                        'end_time': '2019-01-12',
                        'week_day': 2,
                        'time': '21:43:23'}
        result = notification_data_validator(data=invalid_data, update=True)
        self.assertFalse(result)

        invalid_data = {'start_time': '2019-01-12',
                        'end_time': 'invalid time',
                        'week_day': 2,
                        'time': '21:43:23'}
        result = notification_data_validator(data=invalid_data, update=True)
        self.assertFalse(result)

        invalid_data = {'start_time': '2019-01-12',
                        'end_time': '2019-02-12',
                        'week_day': -1,
                        'time': '21:43:23'}
        result = notification_data_validator(data=invalid_data, update=True)
        self.assertFalse(result)

        invalid_data = {'start_time': '2019-01-12',
                        'end_time': '2019-02-12',
                        'week_day': 3,
                        'time': 'invalid time'}
        result = notification_data_validator(data=invalid_data, update=True)
        self.assertFalse(result)

        test_data = {'start_time': '2019-01-12',
                     'end_time': '2019-02-12',
                     'week_day': 3,
                     'time': '21:43:23'}
        result = notification_data_validator(data=test_data, update=True)
        self.assertTrue(result)

    def test_place_data_validator(self):
        """Method that tests the place_data_validator function"""
        invalid_data = {'longitude': 42.124,
                        'latitude': 42.124}
        result = place_data_validator(data=invalid_data)
        self.assertFalse(result)

        invalid_data = {'longitude': 42.124,
                        'latitude': 42.124,
                        'address': None}
        result = place_data_validator(data=invalid_data)
        self.assertFalse(result)

        invalid_data = {'longitude': 'invalid longitude',
                        'latitude': 42.124,
                        'address': 'some address',
                        'name': 'some name',
                        'stop_id': 4231}
        result = place_data_validator(data=invalid_data, update=True)
        self.assertFalse(result)

        invalid_data = {'longitude': 42.124,
                        'latitude': 'invalid latitude',
                        'address': 'some address',
                        'name': 'some name',
                        'stop_id': 4231}
        result = place_data_validator(data=invalid_data, update=True)
        self.assertFalse(result)

        invalid_data = {'longitude': 42.124,
                        'latitude': 42.452,
                        'address': 123,
                        'name': 'some name',
                        'stop_id': 4231}
        result = place_data_validator(data=invalid_data, update=True)
        self.assertFalse(result)

        invalid_data = {'longitude': 42.124,
                        'latitude': 42.452,
                        'address': 'some address',
                        'name': 123,
                        'stop_id': 4231}
        result = place_data_validator(data=invalid_data, update=True)
        self.assertFalse(result)

        invalid_data = {'longitude': 42.124,
                        'latitude': 42.452,
                        'address': 'some address',
                        'name': 'some name',
                        'stop_id': 'invalid stop_id'}
        result = place_data_validator(data=invalid_data, update=True)
        self.assertFalse(result)

        test_data = {'longitude': 42.124,
                     'latitude': 42.452,
                     'address': 'some address',
                     'name': 'some name',
                     'stop_id': 4231}
        result = place_data_validator(data=test_data, update=True)
        self.assertTrue(result)

    def test_route_data_validator(self):
        """Method that tests the route_data_validator function"""
        invalid_data = {'time': '21:43:23'}
        result = route_data_validator(data=invalid_data)
        self.assertFalse(result)

        invalid_data = {'time': '21:43:23',
                        'position': None}
        result = route_data_validator(data=invalid_data)
        self.assertFalse(result)

        invalid_data = {'time': 'invalid time',
                        'position': 1,
                        'transport_id': 4321}
        result = route_data_validator(data=invalid_data, update=True)
        self.assertFalse(result)

        invalid_data = {'time': '21:43:23',
                        'position': 'invalid position',
                        'transport_id': 4321}
        result = route_data_validator(data=invalid_data, update=True)
        self.assertFalse(result)

        invalid_data = {'time': '21:43:23',
                        'position': 1,
                        'transport_id': 'invalid transport_id'}
        result = route_data_validator(data=invalid_data, update=True)
        self.assertFalse(result)

        test_data = {'time': '21:43:23',
                     'position': 1,
                     'transport_id': 4321}
        result = route_data_validator(data=test_data, update=True)
        self.assertTrue(result)

    def test_way_data_validator(self):
        """Method that tests the way_data_validator function"""
        invalid_data = {'name': 123}
        result = way_data_validator(data=invalid_data)
        self.assertFalse(result)

        test_data = {'name': 'some name'}
        result = way_data_validator(data=test_data)
        self.assertTrue(result)

    def test_email_validator(self):
        """Method that tests the email_validator function"""
        invalid_email = 123
        result = email_validator(email=invalid_email)
        self.assertFalse(result)

        invalid_email = 'bad_email'
        result = email_validator(email=invalid_email)
        self.assertFalse(result)

        test_email = 'email@mail.com'
        result = email_validator(email=test_email)
        self.assertTrue(result)

    def test_password_validator(self):
        """Method that tests the email_validator function"""
        invalid_password = 123
        result = password_validator(password=invalid_password)
        self.assertFalse(result)

        invalid_password = 'bad_password'
        result = password_validator(password=invalid_password)
        self.assertFalse(result)

        test_password = '123456Aa'
        result = password_validator(password=test_password)
        self.assertTrue(result)

    def test_credentials_validator(self):
        """Method that tests the credentials_validator function"""
        invalid_data = {'email': 123}
        result = credentials_validator(data=invalid_data)
        self.assertFalse(result)

        invalid_data = {'email': 123,
                        'password': None}
        result = credentials_validator(data=invalid_data)
        self.assertFalse(result)

        invalid_data = {'email': 123,
                        'password': 123}
        result = credentials_validator(data=invalid_data, update=True)
        self.assertFalse(result)

        invalid_data = {'email': 'email@mail.com',
                        'password': 123}
        result = credentials_validator(data=invalid_data, update=True)
        self.assertFalse(result)

        test_data = {'email': 'email@mail.com',
                     'password': '123456Aa'}
        result = credentials_validator(data=test_data, update=True)
        self.assertTrue(result)

    def test_profile_validator(self):
        """Method that tests the profile_validator function"""
        invalid_data = {'first_name': 123}
        result = profile_validator(data=invalid_data)
        self.assertFalse(result)

        invalid_data = {'first_name': 'test',
                        'last_name': 123}
        result = profile_validator(data=invalid_data)
        self.assertFalse(result)

        test_data = {'first_name': 'test',
                     'last_name': 'test'}
        result = profile_validator(data=test_data)
        self.assertTrue(result)

    def test_phone_validator(self):
        """Method that tests the phone_validator function"""
        invalid_phone = 123
        result = phone_validator(phone=invalid_phone)
        self.assertFalse(result)

        invalid_phone = '123'
        result = phone_validator(phone=invalid_phone)
        self.assertFalse(result)

        test_phone = '+380123456789'
        result = phone_validator(phone=test_phone)
        self.assertTrue(result)
