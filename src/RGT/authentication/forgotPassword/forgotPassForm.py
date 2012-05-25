from django.contrib.auth.models import User
from django import forms

class ForgotPassForm(forms.Form):
    email = forms.EmailField(label= 'Enter your email address:');
    
    def clean_email(self):
        data = self.cleaned_data['email']
    
        try:
            User.objects.get(email= data)
        except User.DoesNotExist:
            raise forms.ValidationError('This email address is not registered.')
    
        return data