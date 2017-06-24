from django import forms
from .. import CaptchaVerifier


class CaptchaSecuredForm(forms.Form):
    captchaVerifier = CaptchaVerifier()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CaptchaSecuredForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.captchaVerifier.verify_captcha(self.request):
            return super(CaptchaSecuredForm, self).clean()

        raise forms.ValidationError('Captcha verification failed.')