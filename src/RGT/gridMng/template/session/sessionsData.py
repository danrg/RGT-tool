from ...models import Session

from ...template.gridTableData import GridTableData
from ...template.session.participantsData import ParticipantsData
from ...utility import generateGridTable, generateRandomString
from ...session.state import State as SessionState


class SessionsData(object):
    participating_sessions = None
    facilitating_sessions = None
    pending_responses = None
    session = None

    def __init__(self, user, session=None):
        self.participating_sessions = Session.objects.with_participation(user)
        self.facilitating_sessions = Session.objects.with_facilitator(user)
        self.pending_responses = Session.objects.with_pending_responses(user)
        self.session = session


class ParticipatingSessionsData(SessionsData):
    pass


class MySessionsContentData(SessionsData):
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
            self.participantTableData = ParticipantsData(session=session)
            self.iterations_with_results = session.get_iterations_with_results()

            if session.state.name == SessionState.CHECK:
                self.showRequestButtons = True
                self.showCloseSessionButton = True
                self.saveGridSession = True
                grid_template_data.changeRatingsWeights = True
                grid_template_data.changeCornAlt = True
                grid_template_data.checkForTableIsSave = True
