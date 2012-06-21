from django import forms

class GeneralsForm(forms.Form):
    grid_name = forms.CharField(widget=forms.TextInput(attrs={'size':'45'}))
    description = forms.CharField(widget=forms.Textarea, required=False)
    
class AlternativesForm(forms.Form):
    # override the init in order to dynamically add fields to the form in order to be saved,
    # the fields are saved only when the user selects submit
    def __init__(self, *args, **kwargs):
        super(AlternativesForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            for x in range(int(self.data['num-alternatives'])):
                alternativeName = 'alternative%d' % (x+1)
                # every time, alternative fields are added with the name 'alternative..', and this because
                # Django always adds '1-' % (where 1 the number of the step with zero index) prefix in the name,
                # with this the names are kept always the same
                self.fields[alternativeName] = forms.CharField()
    
class ConcernsForm(forms.Form):
    # override the init in order to dynamically add fields to the form in order to be saved,
    # the fields are saved only when the user selects submit
    def __init__(self, *args, **kwargs):
        super(ConcernsForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            for x in range(int(self.data['num-concerns'])):
                left_concern_name = 'concern%d-left' % (x+1)
                right_concern_name = 'concern%d-right' % (x+1)
                # every time, concern fields are added with the names 'concern..-left' and 'concern..-right', and this because
                # Django always adds '2-' % (where 2 the number of the step with zero index) prefix in the name,
                # with this the names are kept always the same
                self.fields[left_concern_name] = forms.CharField()
                self.fields[right_concern_name] = forms.CharField()
    
class WeightsForm(forms.Form):
    # override the init in order to dynamically add fields to the form in order to be saved,
    # the fields are saved only when the user selects submit
    def __init__(self, *args, **kwargs):
        super(WeightsForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            for x in range(int(self.data['num-weights'])):
                weight_name = 'weight%d' % (x+1)
                # every time, weight fields are added with the name 'weight..', and this because
                # Django always adds '3-' % (where 3 the number of the step with zero index) prefix in the name,
                # with this the names are kept always the same
                self.fields[weight_name] = forms.FloatField()
    
class RatingsForm(forms.Form):
    # override the init in order to dynamically add fields to the form in order to be saved,
    # the fields are saved only when the user selects submit
    def __init__(self, *args, **kwargs):
        super(RatingsForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            for x in range(int(self.data['num-alternatives'])):
                for z in range(int(self.data['num-concerns'])):
                    rating_name = 'rating-concern%d-alternative%d' % ((z+1), (x+1))
                    # every time, rating fields are added with the name 'rating-concern..-alternative..', and this because
                    # Django always adds '4-' % (where 4 the number of the step with zero index) prefix in the name,
                    # with this the names are kept always the same
                    self.fields[rating_name] = forms.CharField(widget=forms.HiddenInput())