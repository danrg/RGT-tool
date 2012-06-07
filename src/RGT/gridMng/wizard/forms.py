from django import forms

class GeneralsForm(forms.Form):
    grid_name = forms.CharField()
    description = forms.CharField(widget=forms.Textarea, required=False)
    
class AlternativesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(AlternativesForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            for x in range(int(self.data['numAlternatives'])):
                alternativeName = 'alternative%d' % (x+1)
                value = 'alternative%d'%(x+1)
                # after the first time of submitting the form, Django adds '1-' prefix to
                # the alternatives names, and thats why the names are checked, in order to get
                # the data of the form.data with the correct key.
                if '1-%s' % alternativeName in self.data.keys():
                    value = '1-alternative%d'%(x+1)
                # every time alternative fields are added with the name 'alternative..'
                self.fields[alternativeName] = forms.CharField(
                            widget=forms.TextInput()) #attrs={'value':self.data[value]}
    
class ConcernsForm(forms.Form):
    concern = forms.CharField()
    
class WeightsForm(forms.Form):
    weight = forms.CharField()
    
class RatingsForm(forms.Form):
    rating = forms.CharField()