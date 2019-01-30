"""This module provides helper functions to send SMS and emails."""

from smtplib import SMTPRecipientsRefused
import nexmo

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


def send_email(to_email, html_message, mail_subject, message):
    """Function that provides sending email to the user"""
    try:
        send_mail(subject=mail_subject,
                  message=message,
                  html_message=html_message,
                  from_email=settings.DEFAULT_FROM_EMAIL,
                  recipient_list=to_email)

    except SMTPRecipientsRefused:
        return False
    return True
