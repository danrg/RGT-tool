'''
Created on 9 apr. 2012

@author: Gray
'''


class UserAlreadyParticipating(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)