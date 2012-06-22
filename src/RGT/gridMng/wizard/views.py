from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from RGT.gridMng.views import createGrid
from RGT.gridMng.models import Grid

class GridWizard(SessionWizardView):

    def get_template_names(self):
        # Get the templates to be used for the steps of the wizard
        return ['gridMng/wizard/gridWizard_step%d.html' % (self.steps.step1)]
    
    def get_context_data(self, form, **kwargs):
        context = super(GridWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.step1 == 3:
            # Get the alternatives data from step 1 (zero index) if the process is on step 3 (one index)
            # in order to generate the alternatives list
            try:
                context.update({'alternatives_data':self.get_cleaned_data_for_step('1')})
            except:
                #
                pass
        elif self.steps.step1 == 4:
            # Get the concerns data from step 2 (zero index) if the process is on step 4 (one index)
            # in order to generate the weight inputs according to this data
            context.update({'concerns_data':self.get_cleaned_data_for_step('2')})
        elif self.steps.step1 == 5:
            # Get the alternatives data from step 1 (zero index) and the concerns data from step 2 (zero index)
            # if the process is on step 5 (one index), in order to generate the alternatives list, the concerns list,
            # and the hidden fields with the number of alternatives and concerns, so the user can select rating values
            context.update({'alternatives_data':self.get_cleaned_data_for_step('1'),
                            'concerns_data':self.get_cleaned_data_for_step('2')})
        return context  

    def done(self, form_list, **kwargs):
        # Get the data of the form, create the grid and redirect to 'grids' page
        # the data are supposed to be validated, so no validation is needed here
        # Construct the step data and the prefixes (steps are zero index)
        # step 0
        step_zero_data = self.get_form_step_data(form_list[0])
        step_zero_prefix = self.get_form_prefix(step='0', form=form_list[0])
        # step 1
        step_one_data = self.get_form_step_data(form_list[1])
        step_one_prefix = self.get_form_prefix(step='1', form=form_list[1])
        # step 2
        step_two_data = self.get_form_step_data(form_list[2])
        step_two_prefix = self.get_form_prefix(step='2', form=form_list[2])
        # step 3
        step_three_data = self.get_form_step_data(form_list[3])
        step_three_prefix = self.get_form_prefix(step='3', form=form_list[3])
        # step 4
        step_four_data = self.get_form_step_data(form_list[4])
        step_four_prefix = self.get_form_prefix(step='4', form=form_list[4])
        # Get the user of the request
        user_obj = self.request.user
        # The grid type is 'User', because the grid is created through the wizard
        grid_type = Grid.GridType.USER_GRID
        # Get the grid name of the form data of step 0 (zero index)
        grid_name = step_zero_data['%s-grid_name' % (step_zero_prefix)]
        # Get the number concerns from the form data of step 2 (zero index)
        num_concerns = step_two_data['num-concerns']
        # Get the number concerns from the form data of step 1 (zero index)
        num_alternatives = step_one_data['num-alternatives']
        # Get the alternative values from the form data of step 1 (zero index)
        alternative_values = []
        for i in range(int(num_alternatives)):
            val = (step_one_data['%s-alternative%d' % (step_one_prefix, i+1)]).strip()
            alternative_values.append(val)
        # Get the concern and weight values from the form data of step 2 for concerns, and step 3 for weights (zero index)
        concern_values = []
        for i in range(int(num_concerns)):
            left = (step_two_data['%s-concern%d-left' % (step_two_prefix, i+1)]).strip()
            right = (step_two_data['%s-concern%d-right' % (step_two_prefix, i+1)]).strip()
            weight = step_three_data['%s-weight%d' % (step_three_prefix, i+1)]
            concern_values.append((left, right, weight))
        # Get the rating values from the form data of step 4 (zero index)
        rating_values = []
        for i in range(int(num_concerns)):
            ratings = []
            for j in range(int(num_alternatives)):
                rating = float(step_four_data['%s-rating-concern%d-alternative%d' % (step_four_prefix, i+1, j+1)])
                ratings.append(rating)
            rating_values.append(ratings)
        # We want to create ratings
        create_ratings = True
        createGrid(user_obj, grid_type, grid_name, num_concerns, num_alternatives, concern_values, alternative_values, rating_values, create_ratings)
        return HttpResponseRedirect('/grids/')