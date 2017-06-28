from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from types import StringType


class HkernNode(BasicSvgNode):
    svgNodeType = BasicSvgNode.SVG_HKERN_NODE

    ATTRIBUTE_U1 = 'u1'
    ATTRIBUTE_G1 = 'g1'
    ATTRIBUTE_U2 = 'u2'
    ATTRIBUTE_G2 = 'g2'
    ATTRIBUTE_K = 'k'

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'hkern')

    def setU1(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_U1, data)

    def setG1(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_G1, data)

    def setU2(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_U2, data)

    def setG2(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_G2, data)

    def setK(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_K, data)

    def getU1(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_U1)
        if node is not None:
            return node.nodeValue
        return None

    def getG1(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_G1)
        if node is not None:
            return node.nodeValue
        return None

    def getU2(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_U2)
        if node is not None:
            return node.nodeValue
        return None

    def getG2(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_G2)
        if node is not None:
            return node.nodeValue
        return None

    def getK(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_K)
        if node is not None:
            return node.nodeValue
        return None
        