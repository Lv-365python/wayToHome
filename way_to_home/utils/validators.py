"""
Project validators
==================
Module that provides validation functions for all kinds of project's data
"""
import datetime
import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email

DATE_MASK = ['%Y%m%d', '%Y-%m-%d', '%d-%m-%Y', '%d%m%Y', '%m%d%Y', '%d/%m/%Y']
TIME_MASK = "%H:%M:%S"
PASSWORD_REG_EXP = r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]*$'


def string_validator(value, min_length=0, max_length=None):
    """Provide string validation."""

    if not isinstance(value, str):
        return False

    if len(value) < min_length:
        return False

    if max_length:
        if len(value) > max_length:
            return False

    return True


def coordinate_validator(value, min_value, max_value):
    """Provide coordinate validation"""

    if not isinstance(value, float):
        return False

    if not min_value <= value <= max_value:
        return False

    return True


def required_keys_validator(data, keys_required):
    """Provide required keys validation"""
    keys = set(data.keys())
    keys_required = set(keys_required)

    return not keys_required.difference(keys)


def none_validator_for_required_keys(data, keys_required):
    for key, value in data.items():
        if key in keys_required and value is None:
            return False
    return True


def date_validator(date):
    """Function that provides validation data type"""
    for mask in DATE_MASK:
        try:
            date = datetime.datetime.strptime(date, mask).date()
            return date
        except ValueError:
            pass


def start_date_validator(start_date):
    """Function validates start_date field"""
    today = datetime.date.today()
    start_date = date_validator(start_date)
    if not start_date:
        return False
    if today > start_date:
        return False

    return True


def end_date_validator(end_date, start_date):
    """Function validates end_date field"""
    start_date = date_validator(start_date) if start_date else datetime.date.today()
    end_date = date_validator(end_date)
    if not (start_date or end_date):
        return False
    if start_date > end_date:
        return False

    return True


def time_validator(time):
    """Function validates time field in Notification model"""
    try:
        datetime.datetime.strptime(time, TIME_MASK)
    except ValueError:
        return False

    return True


def week_day_validator(week_day):
    """Function validates week_day field"""
    if not isinstance(week_day, int):
        return False
    if week_day not in range(0, 7):
        return False

    return True


def notification_data_validator(data, update=False):
    """Function that provides update notification model data validation"""
    required_fields = ['start_time', 'end_time', 'week_day', 'time']

    if not update:
        if not none_validator_for_required_keys(data, required_fields):
            return False
        if not required_keys_validator(data, required_fields):
            return False

    notification_model_fields = [
        'start_time',
        'end_time',
        'week_day',
        'time'
    ]

    filtered_data = {key: data.get(key) for key in notification_model_fields}
    validation_rules = {
        'start_time': start_date_validator,
        'end_time': lambda val: end_date_validator(val, data.get('start_time')),
        'week_day': week_day_validator,
        'time': time_validator,
    }

    for key, value in filtered_data.items():
        if value is not None:
            if not validation_rules[key](value):
                return False

    return True


def place_data_validator(data, update=False):
    """Provide data validation before create/update place object"""
    required_fields = ['longitude', 'latitude', 'address']

    if not update:
        if not none_validator_for_required_keys(data, required_fields):
            return False
        if not required_keys_validator(data, required_fields):
            return False

    place_model_fields = [
        'longitude',
        'latitude',
        'address',
        'name',
        'stop_id',
    ]

    filtered_data = {key: data.get(key) for key in place_model_fields}
    validation_rules = {
        'address': lambda val: string_validator(val, max_length=255),
        'name': lambda val: string_validator(val, max_length=255),
        'stop_id': lambda val: isinstance(val, int) and val > 0,
        'longitude': lambda val: coordinate_validator(val, min_value=-180, max_value=180),
        'latitude': lambda val: coordinate_validator(val, min_value=-90, max_value=90),
    }

    for key, value in filtered_data.items():
        if value is not None:
            if not validation_rules[key](value):
                return False

    return True


def route_data_validator(data, update=False):
    """Provide data validation before create/update route object"""
    required_fields = ['time', 'position']

    if not update:
        if not none_validator_for_required_keys(data, required_fields):
            return False
        if not required_keys_validator(data, required_fields):
            return False

    route_model_fields = [
        'time',
        'position',
        'transport_id'
    ]

    filtered_data = {key: data.get(key) for key in route_model_fields}
    validation_rules = {
        'position': lambda val: isinstance(val, int) and val >= 0,
        'transport_id': lambda val: isinstance(val, int) and val >= 0,
        'time': time_validator
    }

    for key, value in filtered_data.items():
        if value is not None:
            if not validation_rules[key](value):
                return False

    return True


def way_data_validator(data):
    """Function that provides way model data validation"""
    if not string_validator(data.get('name'), min_length=1, max_length=128):
        return False
    return True


def email_validator(email):
    """Function that provides email validation"""
    if not string_validator(email, max_length=64):
        return False
    try:
        validate_email(email)
    except (ValidationError, AttributeError):
        return False
    return True


def password_validator(password):
    """Function that provides password validation"""
    if not string_validator(password, max_length=128):
        return False
    try:
        template = re.compile(PASSWORD_REG_EXP)
        if not template.match(password):
            return False
    except (TypeError, AttributeError):
        return False
    return True


def credentials_validator(data, update=False):
    """Function that provides registration and log in validation"""
    required_fields = ['email', 'password']
    if not update:
        if not required_keys_validator(data, required_fields):
            return False
        if not none_validator_for_required_keys(data, required_fields):
            return False
    if not email_validator(data.get('email')):
        return False
    if not password_validator(data.get('password')):
        return False
    return True


def profile_validator(data):
    """Function that provides user_profile data validation"""
    profile_fields = [
        'first_name'
        'last_name'
    ]
    filtered_data = {key: data.get(key) for key in profile_fields}

    validation_rules = {
        'first_name': lambda val: string_validator(val, 64),
        'last_name': lambda val: string_validator(val, 64)
    }

    for key, value in filtered_data.items():
        if value is not None:
            if not validation_rules[key](value):
                return False

    return True
