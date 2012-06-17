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
                # every time alternative fields are added with the name 'alternative..' and this because
                # Django always adds '%d-' % (the number of the step with zero index) prefix in the name.
                # with this the names are kept always the same
                self.fields[alternativeName] = forms.CharField()
    
class ConcernsForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(ConcernsForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            for x in range(int(self.data['numConcernPairs'])):
                left_concern_name = 'concern%d-left' % (x+1)
                right_concern_name = 'concern%d-right' % (x+1)
                # every time alternative fields are added with the name 'alternative..' and this because
                # Django always adds '%d-' % (the number of the step with zero index) prefix in the name.
                # with this the names are kept always the same
                self.fields[left_concern_name] = forms.CharField()
                self.fields[right_concern_name] = forms.CharField()
    
class WeightsForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(WeightsForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            for x in range(int(self.data['numWeights'])):
                weight_name = 'weight%d' % (x+1)
                self.fields[weight_name] = forms.FloatField()
    
class RatingsForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        super(RatingsForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            pass