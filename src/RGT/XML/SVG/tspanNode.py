from RGT.XML.SVG.baseEditableTextNode import BaseEditableTextNode
from RGT.XML.SVG.Attribs.positionAttributes import PositionAttributes
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class TspanNode(BaseEditableTextNode, PositionAttributes):
    svgNodeType = BasicSvgNode.SVG_TSPAN_NODE

    ATTRIBUTE_LENGTH_ADJUST = 'lengthAdjust'
    ATTRIBUTE_DX = 'dx'
    ATTRIBUTE_DY = 'dy'
    ATTRIBUTE_ROTATE = 'rotate'
    ATTRIBUTE_TEXT_LENGTH = 'textLength'

    def __init__(self, ownerDoc, x=None, y=None):
        BaseEditableTextNode.__init__(self, ownerDoc, 'tspan')
        PositionAttributes.__init__(self)
        self.setX(x)
        self.setY(y)
        self._allowedSvgChildNodes.update(
            {self.SVG_A_NODE, self.SVG_ALT_GLYPH_NODE, self.SVG_ANIMATE_NODE, self.SVG_ANIMATE_COLOR_NODE,
             self.SVG_SET_NODE, self.SVG_TREF_NODE, self.SVG_TSPAN_NODE})

    def setLengthAdjust(self, data):
        allowedValues = ['spacing', 'spacingAndGlyphs']

        if data is not None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_LENGTH_ADJUST, data)

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

    def setRotate(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ROTATE, data)

    def setTextLength(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TEXT_LENGTH, data)

    def getLengthAdjust(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_LENGTH_ADJUST)
        if node is not None:
            return node.nodeValue
        return None

    def getDx(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_DX)
        if node is not None:
            return node.nodeValue
        return None

    def getDy(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_DY)
        if node is not None:
            return node.nodeValue
        return None

    def getRotate(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ROTATE)
        if node is not None:
            return node.nodeValue
        return None

    def getTextLength(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_TEXT_LENGTH)
        if node is not None:
            return node.nodeValue
        return None