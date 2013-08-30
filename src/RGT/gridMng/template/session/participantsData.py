class ParticipantsData(object):
    participants = None #list of tulip that is used to generate the table that displays if a user has sent a response or has joined a session. format: [(user, 'cssClass', time), ...] or [(user, 'cssClass'), ...]

    def __init__(self, paticipants=None):
        self.participants = paticipants
        