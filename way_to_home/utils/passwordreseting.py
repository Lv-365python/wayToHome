"""
Password reseting
=========
The module that provides functions for sending reset password letter to user and reseting password.
"""
from utils.send_email import send_email
from way_to_home.settings import DOMAIN


def send_email_password_update(user, token):
    """Function that provides sending update password letter to user."""
    message = f'http://{DOMAIN}/api/v1/user/reset_password/{token}'
    mail_subject = 'Password reset'
    if send_email(mail_subject, message, (user.email,)):
        return True


def send_successful_update_email(user):
    """Function that provides sending successful update letter."""
    mail_subject = 'Password reset'
    message = 'Successful password reset.'
    if send_email(mail_subject, message, (user.email,)):
        return True
