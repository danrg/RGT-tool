from django import forms
from django.contrib.auth.models import User
from RGT.authentication.forms.CaptchaSecuredForm import CaptchaSecuredForm

class RegistrationForm(CaptchaSecuredForm):
    email = forms.EmailField(label='E-mail address')
    firstName = forms.CharField(label='First name')
    lastName = forms.CharField(label='Last name')
    password = forms.CharField(label=(u'Password'), widget=forms.PasswordInput(render_value=False))
    retyped = forms.CharField(label=(u'Confirm Password'), widget=forms.PasswordInput(render_value=False))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()

        password = cleaned_data.get('password')
        retyped = cleaned_data.get('retyped')

        if password and retyped:
            if password != retyped:
                self.errors['retyped'] = self.error_class(['The passwords do not match.'])

                # Remove invalid entries
                if password:
                    del cleaned_data['password']
                if retyped:
                    del cleaned_data['retyped']

        return cleaned_data

    def clean_email(self):
        user = None
        data = self.cleaned_data['email']

        try:
            user = User.objects.get(email= data)
        except User.DoesNotExist: #do nothing
            pass

        if user is not None:
            raise forms.ValidationError('This email address is already registered.')

        return data