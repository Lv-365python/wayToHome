"""
Project validators
==================
Module that provides validation functions for all kinds of project's data.
"""
import re
from datetime import datetime, timedelta

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
    """Provide coordinate validation."""

    if not isinstance(value, float):
        return False

    if not min_value <= value <= max_value:
        return False

    return True


def required_keys_validator(data, keys_required):
    """Provide required keys validation."""
    keys = set(data.keys())
    keys_required = set(keys_required)

    return not keys_required.difference(keys)


def date_validator(date):
    """ Function that provides validation data type"""
    for mask in DATE_MASK:
        try:
            date = datetime.strptime(date, mask)
            return date
        except ValueError:
            pass


def start_date_notification_validator(start_date):
    """Function validates start_date field in Notification model"""
    today = datetime.now() - timedelta(days=1)
    start_date = date_validator(start_date)
    if not start_date:
        return False
    if today > start_date:
        return False

    return True


def end_date_notification_validator(end_date, start_date):
    """Function validates end_date field in Notification model"""
    start_date = date_validator(start_date) if start_date else datetime.now() - timedelta(days=1)
    end_date = date_validator(end_date)
    if not start_date or not end_date:
        return False
    if start_date > end_date:
        return False

    return True


def time_validator(time):
    """Function validates time field in Notification model"""
    try:
        datetime.strptime(time, TIME_MASK)
    except ValueError:
        return False

    return True


def week_day_notification_validator(week_day):
    """Function validates week_day field in Notification model"""
    if isinstance(week_day, int):
        if int(week_day) in range(0, 7):
            return True

    return False


def notification_data_validator(data, update=False):
    """Function that provides update notification model data validation"""
    required_fields = ['start_date', 'end_date', 'week_day', 'time', 'way_id']

    if not update:
        if not required_keys_validator(data, required_fields):
            return False

    notification_model_fields = [
        'start_date',
        'end_date',
        'week_day',
        'time',
        'way_id'
    ]

    filtered_data = {key: data.get(key) for key in notification_model_fields}
    validation_rules = {
        'start_date': start_date_notification_validator,
        'end_date': lambda val: end_date_notification_validator(val, data.get('start_date')),
        'week_day': week_day_notification_validator,
        'time': time_validator,
        'way': lambda val: isinstance(val, int) and val > 0
    }

    for key, value in filtered_data.items():
        if value is not None:
            if not validation_rules[key](value):
                return False

    return True


def place_data_validator(data, update=False):
    """Provide data validation before create/update place object."""
    required_fields = ['longitude', 'latitude', 'address']

    if not update:
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
    """Provide data validation before create/update route object."""
    required_fields = ['way', 'start_place', 'end_place', 'time', 'position']

    if not update:
        if not required_keys_validator(data, required_fields):
            return False

    route_model_fields = [
        'way',
        'start_place',
        'end_place',
        'time',
        'position',
        'transport_id'
    ]

    filtered_data = {key: data.get(key) for key in route_model_fields}
    validation_rules = {
        'way': lambda val: isinstance(val, int) and val > 0,
        'start_place': lambda val: isinstance(val, int) and val > 0,
        'end_place': lambda val: isinstance(val, int) and val > 0,
        'position': lambda val: isinstance(val, int) and val >= 0,
        'transport_id': lambda val: isinstance(val, int) and val > 0,
        'time': time_validator,
    }

    for key, value in filtered_data.items():
        if value is not None:
            if not validation_rules[key](value):
                return False

    return True


def way_name_validator(name):
    """Function that provides way model data validation"""
    if string_validator(name, min_length=1, max_length=128):
        return True
    return False


def email_validator(email):
    """Function that provides email validation."""
    try:
        email = email.lower().strip()
        validate_email(email)
        return True
    except (ValidationError, AttributeError):
        return False


def password_validator(password):
    """Function that provides password validation."""
    try:
        template = re.compile(PASSWORD_REG_EXP)
        if template.match(password):
            return True
        return False
    except (TypeError, AttributeError):
        return False


def registration_validate(data):
    """Function that provides registration validation"""
    required_keys = ['email', 'password']
    if not required_keys_validator(data, required_keys):
        return False
    if not (string_validator(data.get('email')) and email_validator(data.get('email'))):
        return False
    if not (string_validator(data.get('password')) and password_validator(data.get('password'))):
        return False
    return True


def login_validate(data):
    """Function that provides login validation."""
    if not data:
        return False
    if not required_keys_validator(data, ['email', 'password']):
        return False
    if not email_validator(data['email']):
        return False
    return True
