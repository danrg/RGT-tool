from RGT.XML.SVG.structuralNode import StructuralNode
from RGT.XML.SVG.Attribs.conditionalProcessingAttributes import ConditionalProcessingAttributes
from types import StringType

class UseNode(StructuralNode, ConditionalProcessingAttributes):
    
    ATTRIBUTE_TRANSFORM= 'transform'
    ATTRIBUTE_X= 'x'
    ATTRIBUTE_Y= 'y'
    ATTRIBUTE_WIDTH= 'width'
    ATTRIBUTE_HEIGH= 'height'
    ATTRIBUTE_XLING_HREF= 'xlink:href'

    def __init__(self, ownerDoc):
        StructuralNode.__init__(self, ownerDoc, 'use')
        ConditionalProcessingAttributes.__init__(self)
    
    
    def setTransform(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TRANSFORM, data)
    
    def setX(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_X, data)
    
    def setY(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_Y, data)
            
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
    
    def setXlinkHref(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_XLING_HREF, data)
            
     
    def getTransform(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_TRANSFORM)
        if node != None:
            return node.nodeValue
        return None
    
    def getX(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_X)
        if node != None:
            return node.nodeValue
        return None
        
    def getY(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_Y)
        if node != None:
            return node.nodeValue
        return None
    
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
    
    def getXlinkHref(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_XLING_HREF)
        if node != None:
            return node.nodeValue
        return None