"""This module provides send email method"""

from smtplib import SMTPRecipientsRefused

from django.core.mail import send_mail

from way_to_home.settings import DEFAULT_FROM_EMAIL


def send_email(mail_subject, message, to_email):
    """Function that provides sending email to the user"""
    try:
        send_mail(mail_subject, message, DEFAULT_FROM_EMAIL, to_email)
    except SMTPRecipientsRefused:
        return False
    return True
