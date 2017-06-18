# from RGT.gridMng.template.gridTableData import GridTableData


class ParticipatingSessionsContentGridsData(object):
    sessionGridData = None #gridTableDataObject
    previousResponseGridData = None #gridTableDataObject
    responseGridData = None #gridTableDataObject
    displaySessionGrid = False
    displayPreviousResponseGrid = False
    displayResponseGrid = False

    def __init__(self, sessionGridData=None, previousResponseGridData=None, responseGridData=None):
        self.sessionGridData = GridTableData(sessionGridData)
        self.previousResponseGridData = GridTableData(previousResponseGridData)
        self.responseGridData = GridTableData(responseGridData)