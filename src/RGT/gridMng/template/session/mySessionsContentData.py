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
            self.participantTableData = ParticipantsData(session=session)

            if session.state.name == SessionState.CHECK:
                self.showRequestButtons = True
                self.showCloseSessionButton = True
                self.saveGridSession = True
                grid_template_data.changeRatingsWeights = True
                grid_template_data.changeCornAlt = True
                grid_template_data.checkForTableIsSave = True