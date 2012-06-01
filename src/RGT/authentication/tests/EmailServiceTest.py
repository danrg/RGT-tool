from django.test import TestCase
from RGT.authentication.EmailService import EmailService
from mock import Mock, MagicMock

class EmailServiceTest(TestCase):
    def test_sendEmail_calls_send_and_returns_True_on_success(self):
        emailService = EmailService()
        email = Mock()

        result = emailService.sendEmail(email)

        self.assertTrue(result)
        email.send.assert_called_with()
        pass

    def test_sendEmail_returns_False_if_send_raises_an_Exception(self):
        emailService = EmailService()
        email = MagicMock()
        email.send.side_effect = Exception('Some generic exception')

        result = emailService.sendEmail(email)

        self.assertFalse(result)