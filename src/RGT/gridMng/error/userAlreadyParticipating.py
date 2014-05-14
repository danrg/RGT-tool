'''
Created on 9 apr. 2012

@author: Gray
'''


class UserAlreadyParticipating(Exception):
    def __init__(self, user, session):
        self.value = 'User %s already in session %s' % (user, session)

    def __str__(self):
        return repr(self.value)