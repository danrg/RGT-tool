from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType

class AnimationValueAttributes(BasicSvgAttribute):
    
    ATTRIBUTE_CALC_MODE= 'calcMode'
    ATTRIBUTE_VALUES= 'values'
    ATTRIBUTE_KEY_TIMES= 'keyTimes'
    ATTRIBUTE_KEY_SPLINES= 'keySplines'
    ATTRIBUTE_FROM= 'from'
    ATTRIBUTE_TO= 'to'
    ATTRIBUTE_BY= 'by'

    def __init__(self):
        BasicSvgAttribute.__init__(self)
    
    def setCalcMode(self, data):
        allowedValues= ['discrete', 'linear', 'paced', 'spline']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_CALC_MODE, data)
    
    def setValues(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VALUES, data)
    
    def setKeyTimes(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_KEY_TIMES, data)
    
    def setKeySplines(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_KEY_SPLINES, data)
    
    def setFrom(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FROM, data)
    
    def setTo(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TO, data)
    
    def setBy(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_BY, data)
            
    def getCalcMode(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_CALC_MODE)
        if node != None:
            return node.nodeValue
        return None
    
    def getValues(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_VALUES)
        if node != None:
            return node.nodeValue
        return None
    
    def getKeyTimes(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_KEY_TIMES)
        if node != None:
            return node.nodeValue
        return None
    
    def getKeySplines(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_KEY_SPLINES)
        if node != None:
            return node.nodeValue
        return None
    
    def getFrom(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FROM)
        if node != None:
            return node.nodeValue
        return None
    
    def getTo(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_TO)
        if node != None:
            return node.nodeValue
        return None
    
    def getBy(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_BY)
        if node != None:
            return node.nodeValue
        return None