from RGT.XML.SVG.baseShapeNode import BaseShapeNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class CircleNode(BaseShapeNode):
    svgNodeType = BasicSvgNode.SVG_CIRCLE_NODE

    ATTRIBUTE_CX = 'cx'
    ATTRIBUTE_CY = 'cy'
    ATTRIBUTE_R = 'r'

    def __init__(self, ownerDoc, cx=None, cy=None, r=None):
        BaseShapeNode.__init__(self, ownerDoc, 'circle')
        self.setCx(cx)
        self.setCy(cy)
        self.setR(r)

    def setCx(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_CX, data)

    def setCy(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_CY, data)

    def setR(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_R, data)

    def getCx(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_CX)
        if node != None:
            return node.nodeValue
        return None

    def getCy(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_CY)
        if node != None:
            return node.nodeValue
        return None

    def getR(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_R)
        if node != None:
            return node.nodeValue
        return None