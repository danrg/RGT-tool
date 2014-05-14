class WrongGridType(Exception):
    def __init__(self):
        Exception.__init__(self, 'Unexpected type grid found')