from django.contrib.auth.models import User
from django import forms
from RGT.authentication.forms.CaptchaSecuredForm import CaptchaSecuredForm

class ForgotPasswordForm(CaptchaSecuredForm):
    email = forms.EmailField(label='Enter your email address:')

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        data = self.cleaned_data['email']

        try:
            User.objects.get(email=data)
        except User.DoesNotExist:
            raise forms.ValidationError('This email address is not registered.')

        return data