from RGT.XML.SVG.baseTextNode import BaseTextNode
from RGT.XML.SVG.Attribs.xlinkAttributes import XlinkAttributes
from RGT.XML.SVG.Attribs.positionAttributes import PositionAttributes
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class AltGlyphNode(BaseTextNode, XlinkAttributes, PositionAttributes):
    svgNodeType = BasicSvgNode.SVG_ALT_GLYPH_NODE

    ATTRIBUTE_DX = 'dx'
    ATTRIBUTE_DY = 'dy'
    ATTRIBUTE_GLYPH_REF = 'glyphRef'
    ATTRIBUTE_FORMAT = 'format'
    ATTRIBUTE_ROTATE = 'rotate'

    def __init__(self, ownerDoc):
        BaseTextNode.__init__(self, ownerDoc, 'altGlyph')
        XlinkAttributes.__init__(self)
        PositionAttributes.__init__(self)
        self.allowAllSvgNodesAsChildNodes = True

    def setDx(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_DX, data)

    def setDy(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_DY, data)

    def setGlypthRef(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_GLYPH_REF, data)

    def setFormat(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FORMAT, data)

    def setRotate(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ROTATE, data)

    def getDx(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_DX)
        if node is not None:
            return node.nodeValue
        return None

    def getDy(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_DY)
        if node is not None:
            return node.nodeValue

    def getGlypthRef(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_GLYPH_REF)
        if node is not None:
            return node.nodeValue

    def getFormat(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_FORMAT)
        if node is not None:
            return node.nodeValue

    def getRotate(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ROTATE)
        if node is not None:
            return node.nodeValue