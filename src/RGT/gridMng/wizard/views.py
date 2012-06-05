from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView

def set_alternatives(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}
    return cleaned_data.get('alternatives', True)

class GridWizard(SessionWizardView):
    template_name='gridMng/gridWizard.html'

    def get_template_names(self):
        return [ 'gridMng/gridWizard_step{0}.html'.format(self.steps.step1)]

    def done(self, form_list, **kwargs):
        # process data of the form and redirect to success page
        return HttpResponseRedirect('/')