from django import forms

class RecoverPassForm(forms.Form):
    password= forms.CharField(label=(u'Password'),widget=forms.PasswordInput(render_value=False))
    retyped= forms.CharField(label=(u'Retype Password'),widget=forms.PasswordInput(render_value=False))
    
    def clean(self):
        cleaned_data = super(RecoverPassForm, self).clean()

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