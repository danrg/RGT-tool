from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from RGT.gridMng.views import createGrid
from RGT.gridMng.models import Grid

class GridWizard(SessionWizardView):

    def get_template_names(self):
        # get the templates to be used for the steps of the wizard
        return [ 'gridMng/wizard/gridWizard_step{0}.html'.format(self.steps.step1)]
    
    def get_context_data(self, form, **kwargs):
        context = super(GridWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.step1 == 3:
            # get the alternatives data from step 1 (0 index) if the process is on step 3 (1 index)
            # in order to generate the alternatives list
            try:
                context.update({'alternatives_data':self.get_cleaned_data_for_step('1')})
            except:
                pass
        elif self.steps.step1 == 4:
            # get the concerns data from step 2 (0 index) if the process is on step 4 (1 index)
            # in order to generate the weight inputs according to this data
            context.update({'concerns_data':self.get_cleaned_data_for_step('2')})
        elif self.steps.step1 == 5:
            # get the alternatives data from step 1 (0 index) and the concerns data from step 2 (0 index)
            # if the process is on step 5 (1 index) in order to generate the alternatives list, the concerns list
            # and the hidden fields with the number of alternatives and concerns, so the user can select rating values
            context.update({'alternatives_data':self.get_cleaned_data_for_step('1'),
                            'concerns_data':self.get_cleaned_data_for_step('2')})
        return context  

    def done(self, form_list, **kwargs):
        # process data of the form and redirect to 'grids' page
        # get the user of the request
        user_obj = self.request.user
        # the grid type is 'User', because the grid is created through the wizard
        grid_type = Grid.GridType.USER_GRID
        # get the grid name of the form data of step 0 (0 index)
        grid_name = self.get_form_step_data(form_list[0])['0-grid_name']
        # get the number concerns from the form data of step 2 (0 index)
        num_concerns = self.get_form_step_data(form_list[2])['num-concerns']
        # get the number concerns from the form data of step 1 (0 index)
        num_alternatives = self.get_form_step_data(form_list[1])['num-alternatives']
        # get the alternative values from the form data of step 1 (0 index)
        alternative_values = []
        for i in range(int(num_alternatives)):
            val = (self.get_form_step_data(form_list[1])['1-alternative%d' % (i+1)]).strip()
            alternative_values.append(val)
        # get the concern and weight values from the form data of step 2 for concerns, and step 3 for weights (0 index)
        concern_values = []
        for i in range(int(num_concerns)):
            left = (self.get_form_step_data(form_list[2])['2-concern%d-left' % (i+1)]).strip()
            right = (self.get_form_step_data(form_list[2])['2-concern%d-right' % (i+1)]).strip()
            weight = self.get_form_step_data(form_list[3])['3-weight%d' % (i+1)]
            concern_values.append((left, right, weight))
        # get the rating values from the form data of step 4 (0 index)
        rating_values = []
        for i in range(int(num_concerns)):
            ratings = []
            for j in range(int(num_alternatives)):
                rating = float(self.get_form_step_data(form_list[4])['4-rating-concern%d-alternative%d' % (i+1, j+1)])
                ratings.append(rating)
            rating_values.append(ratings)
        # we want to create ratings
        create_ratings = True
        #createGrid(user_obj, grid_type, grid_name, num_concerns, num_alternatives, concern_values, alternative_values, rating_values, create_ratings)
        return HttpResponseRedirect('/grids/')