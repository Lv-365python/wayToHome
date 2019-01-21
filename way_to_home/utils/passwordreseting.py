"""
Password reseting
=========
The module that provides functions for sending reset password letter to user and reseting password.
"""
from utils.senderhelper import send_email
from way_to_home.settings import DOMAIN


def send_email_password_update(user, token):
    """Function that provides sending update password letter to user."""
    message = f'http://{DOMAIN}/api/v1/user/reset_password/{token}'
    mail_subject = 'Password reset'
    if not send_email(mail_subject, message, (user.email,)):
        return False
    return True


def send_successful_update_email(user):
    """Function that provides sending successful update letter."""
    mail_subject = 'Password reset'
    message = 'Successful password reset.'
    if not send_email(mail_subject, message, (user.email,)):
        return False
    return True
