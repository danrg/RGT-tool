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
    
    def clean_password(self):
        email = super(LoginForm, self).clean().get('email')
        password = self.cleaned_data['password']
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError('Invalid password.')
        except User.DoesNotExist:
            # user does not exist
            pass
            
        return password
        
        
        
        