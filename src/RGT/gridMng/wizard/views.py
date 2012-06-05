from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView

def set_alternatives(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('alternatives', True)

class GridWizard(SessionWizardView):
    def done(self, form_list, **kwargs):
        # process data of the form and redirect to success page
        return HttpResponseRedirect('/')