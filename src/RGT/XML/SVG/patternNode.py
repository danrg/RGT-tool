from RGT.XML.SVG.containerNode import ContainerNode
from RGT.XML.SVG.Attribs.conditionalProcessingAttributes import ConditionalProcessingAttributes
from RGT.XML.SVG.Attribs.xlinkAttributes import XlinkAttributes
from RGT.XML.SVG.Attribs.positionAttributes import PositionAttributes
from RGT.XML.SVG.Attribs.sizeAttributes import SizeAttributes
from types import StringType

class MyClass(ContainerNode, PositionAttributes, SizeAttributes, ConditionalProcessingAttributes, XlinkAttributes):

    ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED= 'externalResourcesRequired'
    ATTRIBUTE_VIEW_BOX= 'viewBox'
    ATTRIBUTE_PRESERVE_ASPECT_RATIO= 'preserveAspectRatio'
    ATTRIBUTE_WIDTH= 'width'
    ATTRIBUTE_HEIGHT= 'height'
    ATTRIBUTE_PATTERN_UNITS= 'patternUnits'
    ATTRIBUTE_PATTERN_CONTENT_UNITS= 'patternContentUnits'
    ATTRIBUTE_PATTERN_TRANSFORM= 'patternTransform'

    def __init__(self, ownerDoc):
        ContainerNode.__init__(self, ownerDoc, 'pattern')
        PositionAttributes.__init__(self)
        SizeAttributes.__init__(self)
        ConditionalProcessingAttributes.__init__(self)
        XlinkAttributes.__init__(self)
        
    def setExternalResourcesRequired(self, data):
        allowedValues= ['true', 'false']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED, data)
    
    def setViewBox(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VIEW_BOX, data)
    
    def setPreserveAspectRatio(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_PRESERVE_ASPECT_RATIO, data)
    
    def setPatternUnits(self, data):
        allowedValues= ['userSpaceOnUse', 'objectBoundingBox']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_PATTERN_UNITS, data)
    
    def setPatternContentUnits(self, data):
        allowedValues= ['userSpaceOnUse', 'objectBoundingBox']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_PATTERN_CONTENT_UNITS, data)
    
    def setPatternTranform(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_PATTERN_TRANSFORM, data)
    
    def getExternalResourcesRequired(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED)
        if node != None:
            return node.nodeValue
        return None
    
    def getViewBox(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_VIEW_BOX)
        if node != None:
            return node.nodeValue
        return None
    
    def getPreserveAspectRatio(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_PRESERVE_ASPECT_RATIO)
        if node != None:
            return node.nodeValue
        return None
    
    def getPatternUnits(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_PATTERN_UNITS)
        if node != None:
            return node.nodeValue
        return None
    
    def getPatternContentUnits(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_PATTERN_CONTENT_UNITS)
        if node != None:
            return node.nodeValue
        return None
    
    def getPatternTransform(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_PATTERN_TRANSFORM)
        if node != None:
            return node.nodeValue
        return None