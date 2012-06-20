from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView


class GridWizard(SessionWizardView):

    def get_template_names(self):
        return [ 'gridMng/wizard/gridWizard_step{0}.html'.format(self.steps.step1)]
    
    def get_context_data(self, form, **kwargs):
        context = super(GridWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.step1 == 3:
            try:
                context.update({'alternatives_data':self.get_cleaned_data_for_step('1')})
            except:
                pass
        elif self.steps.step1 == 4:
            context.update({'concerns_data':self.get_cleaned_data_for_step('2')})
        elif self.steps.step1 == 5:
            context.update({'alternatives_data':self.get_cleaned_data_for_step('1'),
                            'concerns_data':self.get_cleaned_data_for_step('2')})
        return context
    
#    def process_step(self, form):
#        # if it is the processing of alternatives step
#        if self.steps.step1 == 2:
#            # this is a GridWizard class attribute now, in this way it is possible to
#            # pass data between steps
#            self.alternatives_data = []
#            # construct a dictionary with the alternative data when processing the data
#            # of step2, in order to read them in step3
#            for x in range(int(form.data['numAlternatives'])):
#                alternative_name = '1-alternative%d' % (x+1)
#                self.alternatives_data.append({alternative_name:form.data[alternative_name]})
#            
#        return self.get_form_step_data(form)   

    def done(self, form_list, **kwargs):
        # process data of the form and redirect to success page
        for form in form_list:
            print form.data
        return HttpResponseRedirect('/')