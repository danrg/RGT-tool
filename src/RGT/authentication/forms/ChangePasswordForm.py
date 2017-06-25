from django import forms


class ChangePasswordForm(forms.Form):
    oldPassword = forms.CharField(label='Old password',
                                  widget=forms.PasswordInput(render_value=False))
    newPassword = forms.CharField(label='New password',
                                  widget=forms.PasswordInput(render_value=False))
    retyped = forms.CharField(label='Retype password',
                              widget=forms.PasswordInput(render_value=False))

    # We override the __init__ of the form so we can use the request as parameter
    # so we can check it in its 'clean' method
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()

        old_password = cleaned_data.get('oldPassword')
        new_password = cleaned_data.get('newPassword')
        retyped = cleaned_data.get('retyped')

        if old_password:
            if self.request.user.check_password(old_password):
                if new_password and retyped:
                    if new_password != retyped:
                        self.errors['retyped'] = self.error_class(['The passwords do not match.'])
                        # Remove invalid entries
                        if new_password:
                            del cleaned_data['newPassword']
                        if retyped:
                            del cleaned_data['retyped']
            else:
                self.errors['oldPassword'] = self.error_class(['Invalid password.'])

        return cleaned_data
