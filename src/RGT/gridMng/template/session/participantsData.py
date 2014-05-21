from RGT.gridMng.session.state import State as SessionState

class ParticipantsData(object):
    participants = None #list of tulip that is used to generate the table that displays if a user has sent a response or has joined a session. format: [(user, 'cssClass', time), ...] or [(user, 'cssClass'), ...]

    def __init__(self, session=None):
        if session is not None:
            self.participants = self.__createParticipantPanelData(session)

    def __createParticipantPanelData(self, sessionObj):
        usersAndDateTimes = sessionObj.getRespondents()
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
        