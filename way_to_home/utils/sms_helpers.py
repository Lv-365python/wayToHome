"""This module provides helpers functions for sending SMS."""

import nexmo

from django.conf import settings


def send_sms(phone_number, message):
    """Send message to the specific phone number."""
    client = nexmo.Client(key=settings.NEXMO_API_KEY, secret=settings.NEXMO_API_SECRET)
    response = client.send_message({
        'from': 'Way to Home',
        'to': phone_number,
        'text': message,
        'type': 'unicode'
    })

    response = response['messages'][0]
    if response['status'] != '0':
        return False

    return True
