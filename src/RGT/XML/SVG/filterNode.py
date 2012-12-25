from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.presentationAttributes import PresentationAttributes
from RGT.XML.SVG.Attribs.xlinkAttributes import XlinkAttributes
from RGT.XML.SVG.Attribs.classAttribute import ClassAttribute
from RGT.XML.SVG.Attribs.styleAttribute import StyleAttribute
from RGT.XML.SVG.Attribs.positionAttributes import PositionAttributes
from RGT.XML.SVG.Attribs.sizeAttributes import SizeAttributes
from types import StringType

class FilterNode(BasicSvgNode, PresentationAttributes, XlinkAttributes, ClassAttribute, StyleAttribute, PositionAttributes, SizeAttributes):

    svgNodeType= BasicSvgNode.SVG_FILTER_NODE

    ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED= 'externalResourcesRequired'
    ATTRIBUTE_FILTER_RES= 'filterRes'
    ATTRIBUTE_FILTER_UNITS= 'filterUnits'
    ATTRIBUTE_PRIMITIVE_UNITS= 'primitiveUnits'

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'filter')
        PresentationAttributes.__init__(self)
        XlinkAttributes.__init__(self)
        ClassAttribute.__init__(self)
        StyleAttribute.__init__(self)
        PositionAttributes.__init__(self)
        SizeAttributes.__init__(self)
        #add groups
        self._allowedSvgChildNodes.update(self.SVG_GROUP_DESCRIPTIVE_ELEMENTS, self.SVG_GROUP_FILTER_PRIMITIVE_ELEMENTS)
        #add individual nodes
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_SET_NODE})
        
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
    
    def setFilterRes(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FILTER_RES, data)
    
    def setFilterUnits(self, data):
        allowedValues= ['userSpaceOnUse', 'objectBoundingBox']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_FILTER_UNITS, data)
    
    def setPrimitiveUnits(self, data):
        allowedValues= ['userSpaceOnUse', 'objectBoundingBox']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_PRIMITIVE_UNITS, data)
    
    def getExternalResourcesRequired(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED)
        if node != None:
            return node.nodeValue
        return None
    
    def getFilterRes(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FILTER_RES)
        if node != None:
            return node.nodeValue
        return None
    
    def getFilterUnits(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FILTER_UNITS)
        if node != None:
            return node.nodeValue
        return None
    
    def getPrimitiveUnits(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_PRIMITIVE_UNITS)
        if node != None:
            return node.nodeValue
        return None