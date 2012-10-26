class MySessionsData(object):

    sessions= None #list with tulips containing the session name and usid. format --> [(name, usid), .....]

    def __init__(self, sessions):
        self.sessions= sessions
        