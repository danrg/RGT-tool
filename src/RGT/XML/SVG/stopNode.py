from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.presentationAttributes import PresentationAttributes
from RGT.XML.SVG.Attribs.classAttribute import ClassAttribute
from RGT.XML.SVG.Attribs.styleAttribute import StyleAttribute
from types import StringType


class StopNode(BasicSvgNode, PresentationAttributes, ClassAttribute, StyleAttribute):
    svgNodeType = BasicSvgNode.SVG_STOP_NODE

    ATTRIBUTE_OFFSET = 'offset'

    def __init__(self, ownerDoc, offset=None, stopColor=None, stopOpacity=None, style=None):
        BasicSvgNode.__init__(self, ownerDoc, 'stop')
        PresentationAttributes.__init__(self)
        ClassAttribute.__init__(self)
        StyleAttribute.__init__(self)
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_ANIMATE_COLOR_NODE, self.SVG_SET_NODE})
        self.setOffset(offset)
        self.setStopColor(stopColor)
        self.setStopOpacity(stopOpacity)
        self.setStyle(style)

    def setOffset(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_OFFSET, data)

    def getOffset(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_OFFSET)
        if node != None:
            return node.nodeValue
        return None
        