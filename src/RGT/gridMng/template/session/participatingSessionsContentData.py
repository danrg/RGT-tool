from ...template.gridTableData import GridTableData
from ...models import ResponseGrid


class ParticipatingSessionsContentData(object):
    iterations = None #list containing an integer representing each iteration that is used to create the menu that the participant uses to navigate between response. format [1,2,3,....]
    showNParticipantsAndResponses = None #boolean
    participatingSessionsContentGridsData = None #ParticipatingSessionsContentGridsData object
    responseGrid = None
    session = None
    user = None

    def __init__(self, participation=None):
        if participation is not None:
            self.session = participation.session
            self.user = participation.user
            self.iterations = ResponseGrid.objects.get_iterations_with_grids(self.session, self.user)
            if self.session.state.can_be_responded_to():
                responseGridRelations = ResponseGrid.objects.filter(session=self.session, user=self.user)
                gridTablesData = self.generateParticipatingSessionsGridsData(self.session, self.session.iteration,
                                                                             responseGridRelations)
                self.set_grid_tables_data(gridTablesData)

    def set_grid_tables_data(self, gridTablesData):
        session = self.session
        gridsData = ParticipatingSessionsContentGridsData()
        self.participatingSessionsContentGridsData = gridsData
        gridsData.displaySessionGrid = True
        gridsData.displayResponseGrid = True

        gridsData.sessionGridData = GridTableData(gridTablesData['sessionGridTable'])
        gridsData.sessionGridData.tableId = generateRandomString()
        gridsData.sessionGridData.doesNotShowLegend = True
        # check to see if there is a response table, if so add it
        if 'currentResponseGridTable' in gridTablesData:
            gridsData.responseGridData = GridTableData(
                gridTablesData['currentResponseGridTable'])
        else:
            # if there is no response display a table with the data as seem in the session grid
            gridsData.responseGridData = GridTableData(
                gridTablesData['sessionGridTable'])
            # the weights need to be duplicated in a new object as  the list will be poped later on
            gridsData.responseGridData.weights = gridsData.sessionGridData.weights[:]
        gridsData.responseGridData.tableId = generateRandomString()
        # if the gridTablesData contains a previous response table add it
        if 'previousResponseGrid' in gridTablesData:
            gridsData.previousResponseGridData = GridTableData(gridTablesData['previousResponseGrid'])
            gridsData.previousResponseGridData.tableId = generateRandomString()
            gridsData.previousResponseGridData.doesNotShowLegend = True
            gridsData.displayPreviousResponseGrid = True

        # calculate how many participants there are in this session and how many have sent a response
        self.showNParticipantsAndResponses = True

        if session.state.is_alt_and_con_state():
            gridsData.responseGridData.changeCornAlt = True
            gridsData.responseGridData.doesNotShowLegend = True
        elif session.state.is_ratings_weights_state():
            gridsData.responseGridData.changeRatingsWeights = True
            gridsData.sessionGridData.showRatingWhileFalseChangeRatingsWeights = 'previousResponseGrid' in gridTablesData

        try:
            self.responseGrid = ResponseGrid.objects.get_current(session, self.user)
        except ResponseGrid.DoesNotExist:
            self.responseGrid = None

    def generateParticipatingSessionsGridsData(self, sessionObj, iteration_, responseGridRelation):
        """ This function will generate the data that is needed for the participatingSessionsContentGrids.html template
        returns a dictionary that MAY contain the following keys:  previousResponseGrid, sessionGridTable, currentResponseGridTable
        """
        data = {}
        currentResponseGridRelation = responseGridRelation.filter(iteration=iteration_)

        # a session grid must always be present, if something goes wrong here the calling function should deal with it
        data['sessionGridTable'] = generateGridTable(sessionObj.sessiongrid_set.all()[iteration_].grid)

        # check to see if a previous response grid should be displayed or not
        if iteration_ >= 2 and iteration_ > 1:
            previousResponseGridRelation = responseGridRelation.filter(iteration=iteration_ - 1)
            if len(previousResponseGridRelation) >= 1:
                previousResponseGrid = previousResponseGridRelation[0].grid
                if previousResponseGrid is not None and sessionObj.state.is_equal_to_grid_state(previousResponseGrid):
                    # generate the data for the previous response grid
                    data['previousResponseGrid'] = generateGridTable(previousResponseGridRelation[0].grid)

        # generate response grid data
        # check to see if the user has already send a response grid
        if len(currentResponseGridRelation) >= 1:
            # if he has sent an response generate the data for the grid
            data['currentResponseGridTable'] = generateGridTable(currentResponseGridRelation[0].grid)

        return data