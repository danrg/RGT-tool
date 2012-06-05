from django import forms

class GeneralsForm(forms.Form):
    topic = forms.CharField()
    alternatives = forms.BooleanField(required=False)
    
class AlternativesForm(forms.Form):
    alternative = forms.CharField()
    
class ConcernsForm(forms.Form):
    concern = forms.CharField()
    
class WeightsForm(forms.Form):
    weight = forms.CharField()
    
class RatingsForm(forms.Form):
    rating = forms.CharField()