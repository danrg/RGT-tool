from RGT.XML.SVG.baseGradientNode import BaseGradientNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class RadialGradientNode(BaseGradientNode):
    svgNodeType = BasicSvgNode.SVG_RADIAL_GRADIENT_NODE

    ATTRIBUTE_CX = 'cx'
    ATTRIBUTE_CY = 'cy'
    ATTRIBUTE_R = 'r'
    ATTRIBUTE_FX = 'fx'
    ATTRIBUTE_FY = 'fy'

    def __init__(self, ownerDoc):
        BaseGradientNode.__init__(self, ownerDoc, 'radialGradient')

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

    def setR(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_R, data)

    def setFx(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FX, data)

    def setFy(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FY, data)

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

    def getR(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_R)
        if node is not None:
            return node.nodeValue
        return None

    def getFx(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_FX)
        if node is not None:
            return node.nodeValue
        return None

    def getFy(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_FY)
        if node is not None:
            return node.nodeValue
        return None