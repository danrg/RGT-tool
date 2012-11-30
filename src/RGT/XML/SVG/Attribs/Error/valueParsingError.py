from exceptions import Exception

class ValueParsingError(Exception):

    variableValue= None

    def __init__(self, msg, variableValue):
        Exception.__init__(self, msg)
        
        self.variableValue= variableValue
    
    
    def setVariableValue(self, value):
        self.variableValue= value
        
    def getVariableValue(self):
        return self.variableValue    