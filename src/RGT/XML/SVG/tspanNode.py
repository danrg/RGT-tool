from RGT.XML.SVG.baseTextNode import BaseTextNode
from RGT.XML.SVG.Attribs.positionAttributes import PositionAttributes
from types import StringType

class TspanNode(BaseTextNode, PositionAttributes):

    ATTRIBUTE_LENGTH_ADJUST= 'lengthAdjust'
    ATTRIBUTE_DX= 'dx'
    ATTRIBUTE_DY= 'dy'
    ATTRIBUTE_ROTATE= 'rotate'
    ATTRIBUTE_TEXT_LENGTH= 'textLength'

    def __init__(self, ownerDoc):
        BaseTextNode.__init__(self, ownerDoc, 'tspan')
        PositionAttributes.__init__(self)
        
    def setLengthAdjust(self, data):
        allowedValues= ['spacing', 'spacingAndGlyphs']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_LENGTH_ADJUST, data)
    
    def setDx(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_DX, data)
            
    def setDy(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_DY, data)
    
    def setRotate(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ROTATE, data)
            
    def setTextLength(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TEXT_LENGTH, data)
    
    def getLengthAdjust(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_LENGTH_ADJUST)
        if node != None:
            return node.nodeValue
        return None
    
    def getDx(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_DX)
        if node != None:
            return node.nodeValue
        return None
    
    def getDy(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_DY)
        if node != None:
            return node.nodeValue
        return None
    
    def getRotate(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_ROTATE)
        if node != None:
            return node.nodeValue
        return None
    
    def getTextLength(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_TEXT_LENGTH)
        if node != None:
            return node.nodeValue
        return None