from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType


class PositionAttributes(BasicSvgAttribute):
    ATTRIBUTE_X = 'x'
    ATTRIBUTE_Y = 'y'

    def __init__(self):
        BasicSvgAttribute.__init__(self)


    def setX(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_X, data)

    def setY(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_Y, data)

    def getX(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_X)
        if node is not None:
            return node.nodeValue
        return None

    def getY(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_Y)
        if node is not None:
            return node.nodeValue
        return None
        
        