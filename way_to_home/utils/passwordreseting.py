"""
Password reseting
=========
The module that provides functions for sending reset password letter to user and reseting password.
"""

from django.conf import settings

from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_email_password_update(to_email, template, ctx):
    """Function that provides sending update password letter to user."""
    html_message = render_to_string('emails/' + template, ctx)
    message = 'скинути пароль'
    mail_subject = 'Скинути пароль'

    if not send_mail(mail_subject,
                     message,
                     settings.DEFAULT_FROM_EMAIL,
                     to_email,
                     html_message=html_message):
        return False
    return True


def send_successful_update_email(user):
    """Function that provides sending successful update letter."""
    template = 'update_password.html'
    html_message = render_to_string('emails/' + template)
    mail_subject = 'Відновлення паролю'
    message = 'Успішне відновлення паролю.'

    if not send_mail(mail_subject,
                     message,
                     settings.DEFAULT_FROM_EMAIL,
                     (user.email,),
                     html_message=html_message):
        return False
    return True
