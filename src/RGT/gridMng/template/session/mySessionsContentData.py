from RGT.gridMng.template.gridTableData import GridTableData
from RGT.gridMng.template.session.participantsData import ParticipantsData
from RGT.gridMng.utility import generateGridTable, generateRandomString
from RGT.gridMng.session.state import State as SessionState

class MySessionsContentData(object):
    participantTableData = None #ParticipantsData object, used to grid the table where the facilitator can see who joined the section or responded a request
    tableData = None #gridTableData object
    showRequestButtons = False
    showCloseSessionButton = False
    saveGridSession = False
    session = None

    def __init__(self, session=None):
        if session is not None:
            self.session = session
            sessionGrid = session.get_session_grid()
            grid_template_data = GridTableData(generateGridTable(sessionGrid))
            grid_template_data.showRatingWhileFalseChangeRatingsWeights = session.state.name != SessionState.CHECK
            grid_template_data.tableId = generateRandomString()
            grid_template_data.usid = sessionGrid.usid
            self.tableData = grid_template_data
            self.participantTableData = ParticipantsData(self.__createParticipantPanelData(session))

            if session.state.name == SessionState.CHECK:
                self.showRequestButtons = True
                self.showCloseSessionButton = True
                self.saveGridSession = True
                grid_template_data.changeRatingsWeights = True
                grid_template_data.changeCornAlt = True
                grid_template_data.checkForTableIsSave = True

    def __createParticipantPanelData(self, sessionObj):
        usersAndDateTimes = sessionObj.getUsersThatRespondedRequest()
        participantData = []
        for user in sessionObj.getParticipators():
            # create the list with the user and the class of the css the should be coupled with the user in the html template
            # but first check if the session is in a state where there is no data that can be requested or responded
            if sessionObj.state.name == SessionState.FINISH or sessionObj.state.name == SessionState.INITIAL or sessionObj.state.name == SessionState.CHECK:
                participantData.append((user, 'respondedRequest'))
            else:
                users = []
                dateTimes = []
                for i in range(len(usersAndDateTimes)):
                    users.append(usersAndDateTimes[i]['user'])
                    dateTimes.append(usersAndDateTimes[i]['dateTime'])
                if user in users:
                    j = users.index(user)
                    participantData.append((user, 'respondedRequest', dateTimes[j]))
                else:
                    participantData.append((user, 'didNotRespondedRequest'))
        return participantData