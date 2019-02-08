"""This module provides tests for sender helper module."""

import smtplib

from django.template.loader import render_to_string
from django.test import TestCase
from telebot.apihelper import ApiException
from unittest.mock import patch

from django.conf import settings
from custom_user.models import CustomUser
from utils.jwttoken import create_token
from utils.senderhelper import send_sms, send_email, send_telegram_message


class SenderHelperTestCase(TestCase):
    """TestCase for providing sender helper module testing."""

    def setUp(self):
        """Method that provides preparation before testing sender helper module."""
        self.user = CustomUser.objects.create(
            email='testuser@gmail.com',
            password='testpassword',
            is_active=True
        )

        ctx = {
            'domain': settings.DOMAIN,
            'token': create_token(data={'email': self.user.email})
        }

        self.phone_number = '+380000000000'
        self.message_text = 'test text message'
        self.mail_subject = 'test mail subject'
        self.html_message = render_to_string('emails/' + 'registration.html', ctx)

    @patch('nexmo.Client.send_message')
    def test_send_sms_success(self, nexmo_send_message):
        """Provide tests for `send_email` method in case of success."""
        nexmo_send_message.return_value = {'messages': [{'status': '0'}]}
        successful_sent = send_sms(self.phone_number, self.message_text)
        self.assertTrue(successful_sent)

    @patch('nexmo.Client.send_message')
    def test_send_sms_fail(self, nexmo_send_message):
        """Provide tests for `send_sms` method in case of fail."""
        nexmo_send_message.return_value = {'messages': [{'status': 'fail status'}]}
        successful_sent = send_sms(self.phone_number, self.message_text)
        self.assertFalse(successful_sent)

    @patch('utils.senderhelper.send_mail')
    def test_send_email_success(self, send_email_mock):
        """Provide tests for `send_email` method in case of success."""
        send_email_mock.return_value = True
        successful_sent = send_email(
            (self.user.email,),
            self.html_message,
            self.mail_subject,
            self.message_text
        )
        self.assertTrue(successful_sent)

    @patch('utils.senderhelper.send_mail')
    def test_send_email_fail(self, send_email_mock):
        """Provide tests for `send_email` method in case of fail."""
        send_email_mock.side_effect = smtplib.SMTPRecipientsRefused({})
        successful_sent = send_email(
            (self.user.email,),
            self.html_message,
            self.mail_subject,
            self.message_text
        )
        self.assertFalse(successful_sent)

    @patch('telebot.TeleBot.send_message')
    def test_send_telegram_message_fail(self, send_message):
        """Provide tests for `send_telegram_message` method in case of fail."""
        send_message.side_effect = ApiException('exception_message', 'callback_func', 'test_result')
        successful_sent = send_telegram_message(100, 'test_text')
        self.assertFalse(successful_sent)

    @patch('telebot.TeleBot.send_message')
    def test_send_telegram_message_success(self, send_message):
        """Provide tests for `send_telegram_message` method in case of success."""
        send_message.return_value = True
        successful_sent = send_telegram_message(100, 'test_text')
        self.assertTrue(successful_sent)
