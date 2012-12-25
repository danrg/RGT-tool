from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.presentationAttributes import PresentationAttributes
from RGT.XML.SVG.Attribs.xlinkAttributes import XlinkAttributes
from RGT.XML.SVG.Attribs.classAttribute import ClassAttribute
from RGT.XML.SVG.Attribs.styleAttribute import StyleAttribute
from RGT.XML.SVG.Attribs.positionAttributes import PositionAttributes
from types import StringType

class GlyphRefNode(BasicSvgNode, PresentationAttributes, XlinkAttributes, ClassAttribute, StyleAttribute, PositionAttributes):

    svgNodeType= BasicSvgNode.SVG_GLYPH_REF_NODE

    ATTRIBUTE_DX= 'dx'
    ATTRIBUTE_DY= 'dy'
    ATTRIBUTE_GLYPH_REF= 'glyphRef'
    ATTRIBUTE_FORMAT= 'format'
        

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'glyphRef')
        PresentationAttributes.__init__(self)
        XlinkAttributes.__init__(self)
        ClassAttribute.__init__(self)
        StyleAttribute.__init__(self)
        PositionAttributes.__init__(self)
        self._allowedSvgChildNodes.update({self.SVG_GLYPH_REF_NODE, self.SVG_ALT_GLYPH_ITEM_NODE})
    
    def setDx(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_DX, data)
            
    def setDy(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_DY, data)
    
    def setGlyphRef(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_GLYPH_REF, data)
    
    def setFormat(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FORMAT, data)
    
    def getDx(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_DX)
        if node != None:
            return node.nodeValue
        return None
    
    def getDy(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_DY)
        if node != None:
            return node.nodeValue
        return None
    
    def getGlyphRef(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_GLYPH_REF)
        if node != None:
            return node.nodeValue
        return None
    
    def getFormat(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_FORMAT)
        if node != None:
            return node.nodeValue
        return None