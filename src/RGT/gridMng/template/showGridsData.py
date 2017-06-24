class ShowGridsData(object):
    grids = None #QuerySet object, list of grids that are available to the user

    def __init__(self, grids=None):
        self.grids = grids
