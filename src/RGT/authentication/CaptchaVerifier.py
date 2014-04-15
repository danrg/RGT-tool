import logging
from RGT import settings
from recaptcha.client import captcha
import sys


class CaptchaVerifier(object):
    def verify_captcha(self, request):
        """
        Will use ReCaptcha to verify the captcha submitted in the specified request.

        Will return True if the captcha is valid, False other wise
        """
        challenge = request.POST['recaptcha_challenge_field']
        response = request.POST['recaptcha_response_field']
        privateKey = settings.RECAPTCHA_PRIVATE_KEY
        clientIpAddress = request.META['REMOTE_ADDR']

        try:
            return captcha.submit(challenge, response, privateKey, clientIpAddress).is_valid
        except Exception: # Catch all and log
            logger = logging.getLogger('django')
            logger.error('Unexpected exception from ReCaptcha:' + sys.exc_info()[0])
            return False