class UnableToCreateUSID(Exception):
    def __init__(self, gridName):
        Exception.__init__(self, 'Unable to create unique usid for the grid %s' % gridName)
