from django import forms

TOTAL_WEIGHT = 100
MIN_RATING = 1
MAX_RATING = 5

class GeneralsForm(forms.Form):
    grid_name = forms.CharField(widget=forms.TextInput(attrs={'size':'45'}))
    description = forms.CharField(widget=forms.Textarea(), required=False)
    
class AlternativesForm(forms.Form):
    # Override the initialize in order to dynamically add fields to the form in order to be saved,
    # the fields are saved only when the user selects 'Next Step'.
    def __init__(self, *args, **kwargs):
        super(AlternativesForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            self.num_alternatives = self.data['num-alternatives']
            for x in range(int(self.num_alternatives)):
                alternativeName = 'alternative-%d' % (x+1)
                # Every time, alternative fields are added with the name 'alternative..', and this because django
                # always adds '1-' % (where 1 the number of the step with zero index) prefix in the name,
                # with this the names are kept always the same.
                self.fields[alternativeName] = forms.CharField(widget=forms.TextInput(attrs={'tabindex':'%d'%(x+1),'size':'30'}))
    
    def clean(self):
        cleaned_data = super(AlternativesForm, self).clean()
        alternatives = []
        # Construct a list with the alternatives names.
        for i in range(int(self.num_alternatives)):
            # In case the field with the alternative name has its own validation error then, it is not contained in the
            # cleaned data, thats why we catch the exception.
            try:
                alternative = cleaned_data['alternative-%d' % (i+1)]
                alternatives.append(alternative)
            except:
                # The key does not exist (key=alternative name).
                pass
        # Check if there are duplicate names for the alternatives.
        if len(alternatives) != len(set(alternatives)):
            raise forms.ValidationError('It is not allowed to have the same name for alternatives.')
        return cleaned_data
    
class ConcernsForm(forms.Form):
    # Override the initialize in order to dynamically add fields to the form in order to be saved,
    # the fields are saved only when the user selects 'Next Step'.
    def __init__(self, *args, **kwargs):
        super(ConcernsForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            self.num_concerns = self.data['num-concerns']
            self.num_acrd = self.data['num-acrd']
            for x in range(int(self.num_concerns)):
                left_concern_name = 'concern%d-left' % (x+1)
                right_concern_name = 'concern%d-right' % (x+1)
                # Every time, concern fields are added with the names 'concern..-left' and 'concern..-right', and this because django
                # always adds '2-' % (where 2 the number of the step with zero index) prefix in the name,
                # with this the names are kept always the same.
                self.fields[left_concern_name] = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
                self.fields[right_concern_name] = forms.CharField(widget=forms.TextInput(attrs={'size':'50'}))
            for x in range(int(self.num_acrd)):
                # 'acrd' stands for alternative-concern-relation-data
                acrd_name = 'acrd%d' % (x+1)
                # Every time, hidden acrd fields are added with the names 'acrd..', and this because django
                # always adds '2-' % (where 2 the number of the step with zero index) prefix in the name,
                # with this the names are kept always the same.
                self.fields[acrd_name] = forms.CharField(widget=forms.HiddenInput(attrs={'class':'acrd'}),required=False)
    
    def clean(self):
        cleaned_data = super(ConcernsForm, self).clean()
        concerns = []
        # Construct a list with the concerns names.
        for i in range(int(self.num_concerns)):
            # Name does not exist or in case the field with the concern left pole name has its own validation error then, it is not contained in the
            # cleaned data, thats why we catch the exception.
            try:
                concern_left = cleaned_data['concern%d-left' % (i+1)]
                concerns.append(concern_left)
            except:
                # The key does not exist (key=concern left pole name).
                pass
            # Name does not exist or in case the field with the concern right pole name has its own validation error then, it is not contained in the
            # cleaned data, thats why we catch the exception.
            try:
                concern_right = cleaned_data['concern%d-right' % (i+1)]
                concerns.append(concern_right)
            except:
                # The key does not exist (key=concern right pole name).
                pass
        # Check if there are duplicate names for the concerns names.
        if len(concerns) != len(set(concerns)):
            raise forms.ValidationError('It is not allowed to have the same name for concerns.')
        return cleaned_data
    
class WeightsForm(forms.Form):
    # Override the initialize in order to dynamically add fields to the form in order to be saved,
    # the fields are saved only when the user selects 'Next Step'.
    def __init__(self, *args, **kwargs):
        super(WeightsForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            self.num_weights = self.data['num-weights']
            for x in range(int(self.num_weights)):
                weight_name = 'weight%d' % (x+1)
                # Every time, weight fields are added with the name 'weight..', and this because django
                # always adds '3-' % (where 3 the number of the step with zero index) prefix in the name,
                # with this the names are kept always the same.
                self.fields[weight_name] = forms.FloatField(widget=forms.TextInput(attrs={'size':'3','maxlength':'3','tabindex':'%d'%(x+1)}))
    
    def clean(self):
        cleaned_data = super(WeightsForm, self).clean()
        total = 0
        # Calculate the total weight and if it is more than 100 then return a validation error.
        for i in range(int(self.num_weights)):
            # In case the field with the weight name has its own validation error then, it is not contained in the
            # cleaned data, thats why we catch the exception.
            try:
                weight_name = 'weight%d' % (i+1)
                weight = cleaned_data[weight_name]
                total += float(weight) 
            except:
                # The key does not exist (key=weight name).
                pass
        if total != TOTAL_WEIGHT:
            raise forms.ValidationError('The total weight must be equal to %d.' % TOTAL_WEIGHT) 
        return cleaned_data
    
class RatingsForm(forms.Form):
    # Override the initialize in order to dynamically add fields to the form in order to be saved,
    # the fields are saved only when the user selects 'Next Step'.
    def __init__(self, *args, **kwargs):
        super(RatingsForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            self.num_alternatives = self.data['num-alternatives']
            self.num_concerns = self.data['num-concerns']
            for x in range(int(self.num_alternatives)):
                for z in range(int(self.num_concerns)):
                    rating_name = 'rating-concern%d-alternative%d' % ((z+1), (x+1))
                    # Every time, rating fields are added with the name 'rating-concern..-alternative..', and this because django
                    # always adds '4-' % (where 4 the number of the step with zero index) prefix in the name,
                    # with this the names are kept always the same.
                    self.fields[rating_name] = forms.CharField(widget=forms.HiddenInput())
    
    def clean(self):
        cleaned_data = super(RatingsForm, self).clean()
        value_error = False
        for x in range(int(self.num_alternatives)):
            for z in range(int(self.num_concerns)):
                # In case the field with the rating name has its own validation error then, it is not contained in the
                # cleaned data, thats why we catch the exception.
                try:
                    rating_name = 'rating-concern%d-alternative%d' % ((z+1), (x+1))
                    # Try to convert the string value into float. In case of error then a validation
                    # error is raised.
                    try:
                        value = float(cleaned_data[rating_name])
                        # If the value is outside the desired limits for the ratings, then a validation
                        # error is raised.
                        if value < MIN_RATING or value > MAX_RATING:
                            value_error = True
                            break
                    except:
                        value_error = True
                        break
                except:
                    # The key does not exist (key=rating name).
                    pass
        if value_error:
            raise forms.ValidationError('Rating values are incomplete. Please check the values and submit again.')
        return cleaned_data