from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class FeDisplacementMapNode(BaseFilterNode):
    svgNodeType = BasicSvgNode.SVG_FE_DISPLACEMENT_MAP_NODE

    ATTRIBUTE_IN = 'in'
    ATTRIBUTE_IN2 = 'in2'
    ATTRIBUTE_SCALE = 'scale'
    ATTRIBUTE_X_CHANNEL_SELECTOR = 'xChannelSelector'
    ATTRIBUTE_Y_CHANNEL_SELECTOR = 'yChannelSelector'

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feDisplacementMap')
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_SET_NODE})

    def setIn(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IN, data)

    def setIn2(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IN2, data)

    def setScale(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_SCALE, data)

    def setXChannelSelector(self, data):
        allowedValues = ['R', 'G', 'B', 'A']

        if data != None:
            if type(data) is not StringType:
                data = str(data)

            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_X_CHANNEL_SELECTOR, data)

    def setYChannelSelector(self, data):
        allowedValues = ['R', 'G', 'B', 'A']

        if data != None:
            if type(data) is not StringType:
                data = str(data)

            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_Y_CHANNEL_SELECTOR, data)

    def getIn(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_IN)
        if node != None:
            return node.nodeValue
        return None

    def getIn2(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_IN2)
        if node != None:
            return node.nodeValue
        return None

    def getScale(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_SCALE)
        if node != None:
            return node.nodeValue
        return None

    def getXChannelSelector(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_X_CHANNEL_SELECTOR)
        if node != None:
            return node.nodeValue
        return None

    def getYChannelSelector(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_Y_CHANNEL_SELECTOR)
        if node != None:
            return node.nodeValue
        return None