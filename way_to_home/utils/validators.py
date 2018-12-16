"""
Project validators
==================
Module that provides validation functions for all kinds of project's data.
"""

from datetime import datetime, timedelta


DATE_MASK = ['%Y%m%d', '%Y-%m-%d', '%d-%m-%Y', '%d%m%Y', '%m%d%Y', '%d/%m/%Y']
TIME_MASK = "%H:%M:%S"


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
        return None
    if today > start_date:
        return None

    return True


def end_date_notification_validator(start_date, end_date):
    """Function validates end_date field in Notification model"""
    start_date = date_validator(start_date)
    end_date = date_validator(end_date)
    if not start_date or not end_date:
        return None
    if start_date > end_date:
        return None

    return True


def time_notification_validator(time):
    """Function validates time field in Notification model"""
    try:
        datetime.strptime(time, TIME_MASK)
        return True
    except ValueError:
        pass


def week_day_notification_validator(week_day):
    """Function validates week_day field in Notification model"""
    try:
        if int(week_day) in range(0, 7):
            return True
    except ValueError:
        pass


def notification_create_or_update_validate(data, update=False):
    """Function that provides update notification model data validation"""
    notification_model_fields = ['start_date', 'end_date', 'week_day', 'time']
    filtered_data = {key: data.get(key) for key in notification_model_fields}

    if not update:
        if not required_keys_validator(data, notification_model_fields):
            return False

    validation_rules = {
        'start_date': start_date_notification_validator,
        'end_date': lambda val: end_date_notification_validator(end_date=val, start_date=data.get('start_date')),
        'week_day': week_day_notification_validator,
        'time': time_notification_validator
    }

    for key, value in filtered_data.items():
        if value is not None:
            if not validation_rules[key](value):
                return False

    return True