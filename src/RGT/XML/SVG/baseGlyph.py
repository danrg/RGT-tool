from RGT.XML.SVG.containerNode import ContainerNode
from types import StringType

class BaseGlyph(ContainerNode):

    ATTRIBUTE_D= 'd'
    ATTRIBUTE_HORIZ_ADV_X= 'horiz-adv-x'
    ATTRIBUTE_VERT_ORIGIN_X='vert-origin-x'
    ATTRIBUTE_VERT_ORIGIN_Y= 'vert-origin-y'
    ATTRIBUTE_VERT_ADV_Y= 'vert-adv-y'

    def __init__(self, ownerDoc, tagName):
        ContainerNode.__init__(self, ownerDoc, tagName)
        
    
    def setD(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_D, data)
    
    def setHorizAdvX(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_HORIZ_ADV_X, data)
    
    def setVertOriginX(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VERT_ORIGIN_X, data)
    
    def setVertOriginY(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VERT_ORIGIN_Y, data)
    
    def setVertAdvY(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VERT_ADV_Y, data)
    
    def getD(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_D)
        if node != None:
            return node.nodeValue
        return None
    
    def getHorizAdvX(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_HORIZ_ADV_X)
        if node != None:
            return node.nodeValue
        return None
    
    def getVertOriginX(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_VERT_ORIGIN_X)
        if node != None:
            return node.nodeValue
        return None
    
    def getVertOriginY(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_VERT_ORIGIN_Y)
        if node != None:
            return node.nodeValue
        return None
    
    def getVertAdvY(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_VERT_ADV_Y)
        if node != None:
            return node.nodeValue
        return None