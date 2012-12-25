from RGT.XML.SVG.baseContainerNode import BaseContainerNode
from RGT.XML.SVG.Attribs.conditionalProcessingAttributes import ConditionalProcessingAttributes
from RGT.XML.SVG.Attribs.positionAttributes import PositionAttributes
from RGT.XML.SVG.Attribs.sizeAttributes import SizeAttributes
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class MaskNode(BaseContainerNode, PositionAttributes, SizeAttributes, ConditionalProcessingAttributes):

    svgNodeType= BasicSvgNode.SVG_MASK_NODE

    ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED= 'externalResourcesRequired'
    ATTRIBUTE_MASK_UNITS= 'maskUnits'
    ATTRIBUTE_MASK_CONTENT_UNITS= 'maskContentUnits'

    def __init__(self, ownerDoc):
        BaseContainerNode.__init__(self, ownerDoc, 'mask')
        PositionAttributes.__init__(self)
        SizeAttributes.__init__(self)
        ConditionalProcessingAttributes.__init__(self)
        #add the groups
        self._allowedSvgChildNodes.update(self.SVG_GROUP_ANIMATION_ELEMENTS, self.SVG_GROUP_DESCRIPTIVE_ELEMENTS, self.SVG_GROUP_SHAPE_ELEMENTS, self.SVG_GROUP_STRUCTURAL_ELEMENTS, self.SVG_GROUP_GRADIENT_ELEMENTS)
        #add the individual nodes
        self._allowedSvgChildNodes.update({self.SVG_A_NODE, self.SVG_ALT_GLYPH_DEF_NODE, self.SVG_CLIP_PATH_NODE, self.SVG_COLOR_PROFILE_NODE, self.SVG_CURSOR_NODE, self.SVG_FILTER_NODE,
                                           self.SVG_FONT_NODE, self.SVG_FONT_FACE_NODE, self.SVG_FOREIGN_OBJECT_NODE, self.SVG_IMAGE_NODE, self.SVG_MARKER_NODE, self.SVG_MASK_NODE, self.SVG_PATTERN_NODE,
                                           self.SVG_SCRIPT_NODE, self.SVG_STYLE_NODE, self.SVG_SWITCH_NODE, self.SVG_TEXT_NODE, self.SVG_VIEW_NODE})
    
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
    
    def setMaskUnits(self, data):
        allowedValues= ['userSpaceOnUse', 'objectBoundingBox']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_MASK_UNITS, data)
    
    def setMaskContentUnits(self, data):
        allowedValues= ['userSpaceOnUse', 'objectBoundingBox']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_MASK_CONTENT_UNITS, data)
    
    def getExternalResourcesRequired(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED)
        if node != None:
            return node.nodeValue
        return None
    
    def getMaskUnits(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_MASK_UNITS)
        if node != None:
            return node.nodeValue
        return None
    
    def getMaskContentUnits(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_MASK_CONTENT_UNITS)
        if node != None:
            return node.nodeValue
        return None