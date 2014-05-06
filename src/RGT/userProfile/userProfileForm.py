from django import forms


class UserProfileForm(forms.Form):
    firstName = forms.CharField(label=(u'First name'), required=True)
    lastName = forms.CharField(label=(u'Last name'), required=True)
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone number'}))
    displayHelp = forms.BooleanField(label=(u'Display help icons'), required=False)