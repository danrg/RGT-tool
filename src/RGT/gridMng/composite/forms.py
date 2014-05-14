from django import forms
from RGT.gridMng.models import Grid
from django.contrib.auth.models import User
from RGT.gridMng.template.showGridsData import ShowGridsData

class FirstStepForm(forms.Form):
    composite_name = forms.CharField(widget=forms.TextInput(attrs={'size':'45'}))
    description = forms.CharField(widget=forms.Textarea(), required=False) #No field in database yet

class WhichGridsForm(forms.Form):
#     Override the initialize in order to dynamically add fields to the form in order to be saved,
#     the fields are saved only when the user selects 'Next Step'.
    def __init__(self, *args, **kwargs):
        super(WhichGridsForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            choices2 = ()
            self.num_grids = self.data['num-grids']
            user_name = self.data['user']
            user1 = User.objects.filter(username=user_name)
            gridtype = Grid.GridType.USER_GRID
            templateData = ShowGridsData()
            templateData.grids = Grid.objects.filter(user=user1, grid_type=gridtype)
            i=1
            for grid in templateData.grids:
                gridUsid = grid.usid
                gridName = grid.name
                dummy1 = (str(gridUsid), str(gridName))
                choices2 = (dummy1,) + choices2
                i += 1
            self.fields['gridChoices'] = forms.MultipleChoiceField(required=False, choices=choices2, widget=forms.CheckboxSelectMultiple)

    def clean(self):
        cleaned_data = super(WhichGridsForm, self).clean()

        choices = cleaned_data['gridChoices']
        if len(choices) < 2:
             raise forms.ValidationError('You need to select at least two grids from the list.')

        return cleaned_data

class RulesForm(forms.Form):
     def __init__(self, *args, **kwargs):
        super(RulesForm, self).__init__(*args, **kwargs)
        if len(self.data) > 0:
            self.gridUSid = self.data['gridUSid']