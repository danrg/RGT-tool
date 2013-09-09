from django import forms


class ChangePasswordForm(forms.Form):
    oldPassword = forms.CharField(label=('Old Password'), widget=forms.PasswordInput(render_value=False))
    newPassword = forms.CharField(label=('New Password'), widget=forms.PasswordInput(render_value=False))
    retyped = forms.CharField(label=('Retype Password'), widget=forms.PasswordInput(render_value=False))

    # We override the __init__ of the form so we can use the request as parameter
    # so we can check it in its 'clean' method
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()

        oldPassword = cleaned_data.get('oldPassword')
        newPassword = cleaned_data.get('newPassword')
        retyped = cleaned_data.get('retyped')

        if oldPassword:
            if self.request.user.check_password(oldPassword):
                if newPassword and retyped:
                    if newPassword != retyped:
                        self.errors['retyped'] = self.error_class(['The passwords do not match.'])
                        # Remove invalid entries
                        if newPassword:
                            del cleaned_data['newPassword']
                        if retyped:
                            del cleaned_data['retyped']
            else:
                self.errors['oldPassword'] = self.error_class(['Invalid password.'])

        return cleaned_data