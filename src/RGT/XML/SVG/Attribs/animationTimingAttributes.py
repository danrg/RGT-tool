from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType

class AnimationTimingAttributes(BasicSvgAttribute):

    ATTRIBUTE_BEGIN= 'begin'
    ATTRIBUTE_DUR= 'dur'
    ATTRIBUTE_END= 'end'
    ATTRIBUTE_MIN= 'min'
    ATTRIBUTE_MAX= 'max'
    ATTRIBUTE_RESTART= 'restart'
    ATTRIBUTE_REPEAT_COUNT= 'repeatCount'
    ATTRIBUTE_REPEAT_DUR= 'repeatDur'
    ATTRIBUTE_FILL= 'fill'

    def __init__(self):
        BasicSvgAttribute.__init__(self)
    
    def setBegin(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_BEGIN, data)
    
    def setDur(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_DUR, data)
    
    def setEnd(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_END, data)
    
    def setMin(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_MIN, data)
    
    def setMax(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_MAX, data)
    
    def setRestart(self, data):
        allowedValues= ['always', 'whenNotActive', 'never']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_RESTART, data)
    
    def setRepeatCount(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_REPEAT_COUNT, data)
    
    def setRepeatDur(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_REPEAT_DUR, data)
    
    def setFill(self, data):
        allowedValues= ['freeze', 'remove']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_FILL, data)
    
    def getBegin(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_BEGIN)
        if node != None:
            return node.nodeValue
        return None
    
    def getDur(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_DUR)
        if node != None:
            return node.nodeValue
        return None
    
    def getEnd(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_END)
        if node != None:
            return node.nodeValue
        return None
    
    def getMin(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_MIN)
        if node != None:
            return node.nodeValue
        return None
    
    def getMax(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_MAX)
        if node != None:
            return node.nodeValue
        return None
    
    def getRestart(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_RESTART)
        if node != None:
            return node.nodeValue
        return None
    
    def getRepeatCount(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_REPEAT_COUNT)
        if node != None:
            return node.nodeValue
        return None
    
    def getRepeatDur(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_REPEAT_DUR)
        if node != None:
            return node.nodeValue
        return None
    
    def getFill(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FILL)
        if node != None:
            return node.nodeValue
        return None