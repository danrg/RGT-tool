from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class FeBlendNode(BaseFilterNode):
    svgNodeType = BasicSvgNode.SVG_FE_BLEND_NODE

    ATTRIBUTE_IN = 'in'
    ATTRIBUTE_IN2 = 'in2'
    ATTRIBUTE_MODE = 'mode'

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feBlend')
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_SET_NODE})

    def setIn(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IN, data)

    def setIn2(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IN2, data)

    def setMode(self, data):
        allowedValues = ['normal', 'multiply', 'screen', 'darken', 'lighten']

        if data is not None:
            if type(data) is not StringType:
                data = str(data)

            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_MODE, data)

    def getIn(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_IN)
        if node is not None:
            return node.nodeValue
        return None

    def getIn2(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_IN2)
        if node is not None:
            return node.nodeValue
        return None

    def getMode(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_MODE)
        if node is not None:
            return node.nodeValue
        return None    