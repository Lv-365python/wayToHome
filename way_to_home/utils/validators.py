"""
Project validators
==================
Module that provides validation functions for all kinds of project's data.
"""

import datetime

DATE_MASK = ['%Y%m%d', '%Y-%m-%d', '%d%m%Y', '%m%d%Y']
TIME_MASK = "%H:%M:%S"


def date_validator(date):
    """ Function that provides validation data type"""
    for mask in DATE_MASK:
        try:
            datetime.datetime.strptime(date, mask)
            return True
        except ValueError:
            pass


def start_date_notification_validator(start_date):
    """Function validates start_date field in Notification model"""
    today = datetime.datetime.now()
    if not date_validator(start_date) and today > start_date:
        return None

    return True


def end_date_notification_validator(start_date, end_date):
    """Function validates end_date field in Notification model"""
    if not date_validator(start_date) and start_date > end_date:
        return None

    return True


def time_notification_validator(time):
    """Function validates time field in Notification model"""
    try:
        datetime.datetime.strptime(time, TIME_MASK)
        return True
    except ValueError:
        pass


def week_day_notification_validator(week_day):
    """Function validates week_day field in Notification model"""
    if week_day in range(0, 7):
        return True

    return None
