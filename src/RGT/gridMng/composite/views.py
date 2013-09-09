from django.http import HttpResponseRedirect
from django.contrib.formtools.wizard.views import SessionWizardView
from RGT.gridMng.views import createGrid
from RGT.gridMng.models import Grid
from RGT.gridMng.template.showGridsData import ShowGridsData

class CompositeWizard(SessionWizardView):

    def get_template_names(self):
        # Get the templates to be used for the steps of the wizard.
        return ['gridMng/composite/compositeWizard_step%d.html' % (self.steps.step1)]

    def get_context_data(self, form, **kwargs):
        context = super(CompositeWizard, self).get_context_data(form=form, **kwargs)
        # alternatives step
        if self.steps.step1 == 2:
            try:
                user1 = self.request.user
                gridtype = Grid.GridType.USER_GRID
                templateData = ShowGridsData()
                templateData.grids = Grid.objects.filter(user=user1, grid_type=gridtype)
                templateData.user = user1

                if len(templateData.grids) <= 0:
                    templateData.grids = None

                context.update({'data':templateData})
            except:
                # Alternatives data do not yet exist
                pass

        elif self.steps.step1 == 3:
            try:
                grids_data = self.get_cleaned_data_for_step('1')
                user1 = self.request.user
                gridtype = Grid.GridType.USER_GRID
                templateData = ShowGridsData()
                templateData.grids = Grid.objects.filter(user=user1, grid_type=gridtype, usid__in=grids_data['gridChoices'])

                for x in templateData.grids:
                    print x.name


            except:
                pass

        return context

    def done(self, form_list, **kwargs):
        return HttpResponseRedirect('/grids/')