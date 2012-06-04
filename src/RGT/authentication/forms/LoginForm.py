from django.contrib.auth.models import User
from django import forms

class LoginForm(forms.Form):
    email= forms.EmailField(label= 'E-mail address');
    password= forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False));

    def clean_email(self):
        data = self.cleaned_data['email']

        try:
            User.objects.get(email= data)
        except User.DoesNotExist:
            raise forms.ValidationError('This email address is not registered.')

        return data