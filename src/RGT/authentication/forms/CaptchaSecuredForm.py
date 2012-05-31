from django import forms
from RGT.authentication import CaptchaVerifier

class CaptchaSecuredForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CaptchaSecuredForm, self).__init__(*args, **kwargs)

    def clean(self):
        if CaptchaVerifier().verify_captcha(self.request):
            return super(CaptchaSecuredForm, self).clean()

        raise forms.ValidationError('Captcha verification failed.')