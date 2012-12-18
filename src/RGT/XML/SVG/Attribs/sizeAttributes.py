from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType

class SizeAttributes(BasicSvgAttribute):

    ATTRIBUTE_WIDTH= 'width'
    ATTRIBUTE_HEIGH= 'height'

    def __init__(self):
        BasicSvgAttribute.__init__(self)
        
    
    def setWidth(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_WIDTH, data)
            
    def setHeight(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_HEIGH, data)

    def getWidth(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_WIDTH)
        if node != None:
            return node.nodeValue
        return None
    
    def getHeight(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_HEIGH)
        if node != None:
            return node.nodeValue
        return None