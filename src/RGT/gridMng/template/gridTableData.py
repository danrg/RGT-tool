class GridTableData(object):
    tableId = None #string
    tableHeader = None
    table = None
    weights = None
    hiddenFields = None
    changeCornAlt = False
    doesNotShowLegend = False
    checkForTableIsSave = False
    showRatingWhileFalseChangeRatingsWeights = False
    changeRatingsWeights = False
    usid = None #id of the grid

    def __init__(self, tableData=None):
        if tableData != None:
            if tableData.has_key('table') and tableData.has_key('tableHeader') and tableData.has_key('weights'):
                self.table = tableData['table']
                self.tableHeader = tableData['tableHeader']
                self.weights = tableData['weights']
        