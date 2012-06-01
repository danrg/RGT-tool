from django.test import TestCase
from RGT.authentication.EmailService import EmailService
from mock import Mock

class EmailServiceTest(TestCase):
    def test_sendEmail_calls_send_and_returns_True_on_success(self):
        emailService = EmailService()
        email = Mock()

        result = emailService.sendEmail(email)

        self.assertTrue(result)

        email.send.assert_called_with()
        pass