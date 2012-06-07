from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView


class GridWizard(SessionWizardView):
    template_name='gridMng/gridWizard.html'

    def get_template_names(self):
        return [ 'gridMng/gridWizard_step{0}.html'.format(self.steps.step1)]
    
    def get_context_data(self, form, **kwargs):
        context = super(GridWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.step1 == 3:
            try:
                print self.alternativeData
            except:
                pass
            context.update({'variable': True})
        return context
    
    def process_step(self, form):
        if self.steps.step1 == 2:
            # this is a GridWizard class attribute now, in this way it is possible to
            # pass data between steps
            self.alternativeData={}
            # construct a dictionary with the alternative data when processing the data
            # of step2, in order to read them in step3
            for x in range(int(form.data['numAlternatives'])):
                alternativeName = 'alternative%d' % (x+1)
                value = 'alternative%d'%(x+1)
                if '1-%s' % alternativeName in form.data.keys():
                    value = '1-alternative%d'%(x+1)
                self.alternativeData.update({alternativeName:form.data[value]})
        return self.get_form_step_data(form)

    def done(self, form_list, **kwargs):
        # process data of the form and redirect to success page
        return HttpResponseRedirect('/')