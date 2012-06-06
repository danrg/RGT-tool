from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView

class GridWizard(SessionWizardView):
    template_name='gridMng/gridWizard.html'

    def get_template_names(self):
        return [ 'gridMng/gridWizard_step{0}.html'.format(self.steps.step1)]
    
    def get_context_data(self, form, **kwargs):
        context = super(GridWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.step1 == 3:
            print self.get_form('1').alternatives
            context.update({'variable': True})
        return context
    
    def get_form(self, step=None, data=None, files=None):
        form = super(GridWizard, self).get_form(step, data, files)
        if step == '1':
            form.alternatives = {}
            try:
                for x in range(int(self.request.POST['number-of-alternatives'])):
                    form.alternatives.update({(x+1):self.request.POST['alt-%d'%(x+1)]})
            except:
                pass
        return form

    def done(self, form_list, **kwargs):
        # process data of the form and redirect to success page
        return HttpResponseRedirect('/')