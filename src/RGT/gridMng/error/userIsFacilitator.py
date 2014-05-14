class UserIsFacilitator(Exception):
    def __init__(self, user, session):
        self.value = 'User %s is already the facilitator in session %s' % (user, session)

    def __str__(self):
        return repr(self.value)