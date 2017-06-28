from RGT.XML.SVG.baseShapeNode import BaseShapeNode
from types import StringType


class BasePolyNode(BaseShapeNode):
    ATTRIBUTE_POINTS = 'points'

    def __init__(self, ownerDoc, tagName):
        BaseShapeNode.__init__(self, ownerDoc, tagName)

    def setPoints(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_POINTS, data)

    def getPoints(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_POINTS)
        if node is not None:
            return node.nodeValue
        return None
    
    