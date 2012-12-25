from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.conditionalProcessingAttributes import ConditionalProcessingAttributes
from RGT.XML.SVG.Attribs.graphicalEventAttributes import GraphicalEventAttributes
from RGT.XML.SVG.Attribs.xlinkAttributes import XlinkAttributes
from RGT.XML.SVG.Attribs.presentationAttributes import PresentationAttributes
from RGT.XML.SVG.Attribs.classAttribute import ClassAttribute
from RGT.XML.SVG.Attribs.styleAttribute import StyleAttribute
from RGT.XML.SVG.Attribs.positionAttributes import PositionAttributes
from RGT.XML.SVG.Attribs.sizeAttributes import SizeAttributes
from types import StringType

class ImageNode(BasicSvgNode, ConditionalProcessingAttributes, GraphicalEventAttributes, XlinkAttributes, PresentationAttributes, ClassAttribute, StyleAttribute, PositionAttributes, SizeAttributes):

    svgNodeType= BasicSvgNode.SVG_IMAGE_NODE

    ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED= 'externalResourcesRequired'
    ATTRIBUTE_PRESERVE_ASPECT_RATIO= 'preserveAspectRatio'
    ATTRIBUTE_TRANSFORM= 'transform'

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'image')
        ConditionalProcessingAttributes.__init__(self)
        GraphicalEventAttributes.__init__(self)
        XlinkAttributes.__init__(self)
        PresentationAttributes.__init__(self)
        ClassAttribute.__init__(self)
        StyleAttribute.__init__(self)
        PositionAttributes.__init__(self)
        SizeAttributes.__init__(self)
        self._allowedSvgChildNodes.update(self.SVG_GROUP_ANIMATION_ELEMENTS, self.SVG_GROUP_DESCRIPTIVE_ELEMENTS)
        
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
    
    def setPreserveAspectRatio(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_PRESERVE_ASPECT_RATIO, data)
    
    def setTransform(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TRANSFORM, data)
            
    def getExternalResourcesRequired(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED)
        if node != None:
            return node.nodeValue
        return None
    
    def getPreserveAspectRatio(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_PRESERVE_ASPECT_RATIO)
        if node != None:
            return node.nodeValue
        return None
    
    def getTransform(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_TRANSFORM)
        if node != None:
            return node.nodeValue
        return None