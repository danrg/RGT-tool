from django import forms

class UserProfileForm(forms.Form):
    firstName = forms.CharField(label=(u'First Name'),required=True)
    lastName = forms.CharField(label=(u'Last Name'),required=True)
    address= forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'address'}))
    phone= forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'phone'}))
    displayHelp = forms.BooleanField(label=(u'Display Help Icons'),required=False)