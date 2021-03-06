import itertools

from datetime import datetime
from django.db import transaction
from formtools.wizard.views import SessionWizardView
from django.shortcuts import redirect
from django.utils.timezone import utc

from ...settings import GRID_USID_KEY_LENGTH
from ..prototypes.compositeParse import CompositeParse
from ..template.showGridsData import ShowGridsData
from ..utility import generateRandomString


class CompositeWizard(SessionWizardView):

    def get_template_names(self):
        # Get the templates to be used for the steps of the wizard.
        return ['gridMng/composite/compositeWizard_step%d.html' % self.steps.step1]

    def get_context_data(self, form, **kwargs):
        from ..models import Grid

        context = super(CompositeWizard, self).get_context_data(form=form, **kwargs)
        # From user name, get the user grids for selection
        if self.steps.step1 == 2:
            try:
                user1 = self.request.user
                gridtype = Grid.GridType.USER_GRID
                templateData = ShowGridsData()
                templateData.grids = Grid.objects.filter(user=user1, grid_type=gridtype)
                templateData.user = user1

                if len(templateData.grids) <= 0:
                    templateData.grids = None

                context.update({'data': templateData})
            except:
                # User data do not yet exist
                pass

        elif self.steps.step1 == 3:
            grids_data = self.get_cleaned_data_for_step('1')

            print grids_data

            type = Grid.GridType.USER_GRID
            grids = Grid.objects.filter(user=self.request.user, grid_type=type, usid__in=grids_data['gridChoices'])
            rules = self.create_rules(grids)

            context.update({'grids': grids, 'rules': rules })

        return context

    def done(self, form_list, **kwargs):
        step_zero_data = self.get_form_step_data(form_list[0])
        step_zero_prefix = self.get_form_prefix(step='0', form=form_list[0])

        # step 2 - concerns
        step_two_data = self.get_form_step_data(form_list[2])
        # Get the grid name of the form data of step 0 (zero index).
        grid_name = step_zero_data['%s-composite_name' % step_zero_prefix]
        rules = step_two_data.getlist('rules')
        statuses = step_two_data.getlist('statuses')

        # This is a modified version of 'createGrid' which we are providing the gridUsID beforehand.
        grid = self.createCompositeGrid(self.request.user, grid_name, rules, statuses)

        return redirect(grid)

    def create_rules(self, grids):
        """
        Return a list containing all possible combinations of alternatives from the given grids and the corresponding
        total rating of that combination of alternatives.
        @type grids list of Grid
        """
        from ..models import Rule

        alts = [grid.get_alternative_total_rating_tuples() for grid in grids]
        combinations = itertools.product(*alts)
        rules = []
        for combi in combinations:
            alts, ratings = zip(*combi)
            rules.append(Rule(alts, sum(ratings)))

        rules.sort()

        return rules

    @transaction.atomic
    def createCompositeGrid(self, userObj, gridName, rules, statuses):
        """
        This function is a modificated version of 'createGrid' function.
        What is different is we don't have any numeric values here,
        just alternative names(combinations of valid rules),
        and also we are providing grid.usid beforehand
        """
        from ..models import Composite
        from ..models import Grid
        from ..models import Alternatives
        from ..models import Concerns
        from ..models import Ratings

        if not None in (userObj, rules, statuses):
            gridObj = Grid.objects.create(user=userObj, grid_type=Grid.GridType.COMPOSITE_GRID)
            if gridName is not None:
                gridObj.name = gridName
            gridObj.usid = generateRandomString(GRID_USID_KEY_LENGTH)
            gridObj.dateTime = datetime.utcnow().replace(tzinfo=utc)
            gridObj.save()

            for idx, rule in enumerate(rules):
                parser = CompositeParse(rule)
                compositions = parser.getCompositions()
                status = statuses[idx].lower()
                for composition in compositions:
                    Composite.objects.create(compid=gridObj.usid, user=userObj, rule=composition, status=status)

            alternatives = []
            rules = Composite.objects.filter(compid=gridObj.usid, status="valid")
            for r in rules:
                a = r.rule
                a = a.replace("u'", "")
                alternative = Alternatives.objects.create(grid=gridObj, name=str(a.replace("'", "")))
                alternatives.append(alternative)

            concernValues = [['lc1', 'rc1'], ['lc2', 'rc2'], ['lc3', 'rc3']]
            concerns = []
            for [left, right] in concernValues:
                concern = Concerns.objects.create(grid=gridObj, leftPole=left, rightPole=right)
                concerns.append(concern)

            for concern in concerns:
                for alternative in alternatives:
                    Ratings.objects.create(concern=concern, alternative=alternative)

            return gridObj
        else:
            raise ValueError('One or more variables were None')
