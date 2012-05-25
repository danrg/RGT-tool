class WrongState(Exception):
        
    def __init__(self, value, sessionState=None ):
        self.value= value
        self.state= sessionState
    
    def __str__(self):
        return repr(self.value)