from RGT.XML.SVG.baseShapeNode import BaseShapeNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class EllipseNode(BaseShapeNode):
    svgNodeType = BasicSvgNode.SVG_ELLIPSE_NODE

    ATTRIBUTE_CX = 'cx'
    ATTRIBUTE_CY = 'cy'
    ATTRIBUTE_RX = 'rx'
    ATTRIBUTE_RY = 'ry'

    def __init__(self, ownerDoc, rx=None, ry=None):
        BaseShapeNode.__init__(self, ownerDoc, 'ellipse')
        self.setRx(rx)
        self.setRy(ry)

    def setCx(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_CX, data)

    def setCy(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_CY, data)

    def setRx(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_RX, data)

    def setRy(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_RY, data)

    def getCx(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_CX)
        if node is not None:
            return node.nodeValue
        return None

    def getCy(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_CY)
        if node is not None:
            return node.nodeValue
        return None

    def getRx(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_RX)
        if node is not None:
            return node.nodeValue
        return None

    def getRy(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_RY)
        if node is not None:
            return node.nodeValue
        return None