from RGT.XML.SVG.baseContainerNode import BaseContainerNode
from types import StringType

class BaseGlyph(BaseContainerNode):

    ATTRIBUTE_D= 'd'
    ATTRIBUTE_HORIZ_ADV_X= 'horiz-adv-x'
    ATTRIBUTE_VERT_ORIGIN_X='vert-origin-x'
    ATTRIBUTE_VERT_ORIGIN_Y= 'vert-origin-y'
    ATTRIBUTE_VERT_ADV_Y= 'vert-adv-y'

    def __init__(self, ownerDoc, tagName):
        BaseContainerNode.__init__(self, ownerDoc, tagName)
        #add the groups
        self._allowedSvgChildNodes.update(self.SVG_GROUP_ANIMATION_ELEMENTS, self.SVG_GROUP_DESCRIPTIVE_ELEMENTS, self.SVG_GROUP_SHAPE_ELEMENTS, self.SVG_GROUP_STRUCTURAL_ELEMENTS, self.SVG_GROUP_GRADIENT_ELEMENTS)
        #add the individual nodes
        self._allowedSvgChildNodes.update({self.SVG_A_NODE, self.SVG_ALT_GLYPH_DEF_NODE, self.SVG_CLIP_PATH_NODE, self.SVG_COLOR_PROFILE_NODE, self.SVG_CURSOR_NODE, self.SVG_FILTER_NODE,
                                          self.SVG_FONT_NODE, self.SVG_FONT_FACE_NODE, self.SVG_FOREIGN_OBJECT_NODE, self.SVG_IMAGE_NODE, self.SVG_MARKER_NODE, self.SVG_MASK_NODE, self.SVG_PATTERN_NODE,
                                          self.SVG_SCRIPT_NODE, self.SVG_STYLE_NODE, self.SVG_SWITCH_NODE, self.SVG_TEXT_NODE, self.SVG_VIEW_NODE})
        
    
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