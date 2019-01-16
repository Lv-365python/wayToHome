"""This module provides helper functions to send SMS and emails."""

import nexmo
from smtplib import SMTPRecipientsRefused

from django.conf import settings
from django.core.mail import send_mail


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


def send_email(mail_subject, message, to_email):
    """Function that provides sending email to the user"""
    try:
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, to_email)
    except SMTPRecipientsRefused:
        return False
    return True
