from django import forms

class ContactForm(forms.Form):
    email = forms.EmailField()
    subject = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)