from django import forms
from django.forms.fields import CharField

class GeneralsForm(forms.Form):
    grid_name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea, required=False)
    
class AlternativesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(AlternativesForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            for x in range(int(self.data['numAlternatives'])):
                alternativeName = 'alternative%d' % (x+1);
                self.fields[alternativeName] = CharField()
                print self.data[alternativeName]
            pass


    alternative = forms.CharField()
    
class ConcernsForm(forms.Form):
    concern = forms.CharField()
    
class WeightsForm(forms.Form):
    weight = forms.CharField()
    
class RatingsForm(forms.Form):
    rating = forms.CharField()