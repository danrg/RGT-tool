from RGT.XML.SVG.baseShapeNode import BaseShapeNode
from types import StringType

class LineNode(BaseShapeNode):

    ATTRIBUTE_X1= 'x1'
    ATTRIBUTE_Y1= 'y1'
    ATTRIBUTE_X2= 'x2'
    ATTRIBUTE_Y2= 'y2'

    def __init__(self, ownerDoc, x1= None, y1= None, x2= None, y2= None):
        BaseShapeNode.__init__(self, ownerDoc, 'line')
        self.setX1(x1)
        self.setY1(y1)
        self.setX2(x2)
        self.setY2(y2)
    
    def setX1(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_X1, data)
    
    def setY1(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_Y1, data)
    
    def setX2(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_X2, data)
    
    def setY2(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_Y2, data)
    
    def getX1(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_X1)
        if node != None:
            return node.nodeValue
        return None
    
    def getY1(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_Y1)
        if node != None:
            return node.nodeValue
        return None
    
    def getX2(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_X2)
        if node != None:
            return node.nodeValue
        return None
    
    def getY2(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_Y2)
        if node != None:
            return node.nodeValue
        return None