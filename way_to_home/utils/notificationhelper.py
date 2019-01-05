"""This module provides helpers functions for notifications."""

import nexmo

from way_to_home.settings import NEXMO_API_KEY, NEXMO_API_SECRET


def send_notification(phone_number, minutes):
    """Send notification message to the specific phone number."""
    client = nexmo.Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)
    response = client.send_message({
        'from': 'Way to Home',
        'to': phone_number,
        'text': f'Через {minutes} хвилин прибуде ваш транспорт.',
        'type': 'unicode'
    })

    response = response['messages'][0]
    if response['status'] != '0':
        return False

    return True
