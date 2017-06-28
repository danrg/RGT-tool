from ..utility import generateGridTable


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
        if tableData is not None:
            if tableData.has_key('table') and tableData.has_key('tableHeader') and tableData.has_key('weights'):
                self.table = tableData['table']
                self.tableHeader = tableData['tableHeader']
                self.weights = tableData['weights']


class WritableGridTableData(GridTableData):
    def __init__(self, grid=None):
        table_data = generateGridTable(grid)
        super(WritableGridTableData, self).__init__(tableData=table_data)

        if grid is not None:
            self.usid = grid.usid

        self.changeCornAlt = True
        self.checkForTableIsSave = True
        self.showRatingWhileFalseChangeRatingsWeights = True
        self.changeRatingsWeights = True
