from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class FeCompositeNode(BaseFilterNode):
    svgNodeType = BasicSvgNode.SVG_FE_COMPOSITE_NODE

    ATTRIBUTE_IN = 'in'
    ATTRIBUTE_IN2 = 'in2'
    ATTRIBUTE_OPERATOR = 'operator'
    ATTRIBUTE_K1 = 'k1'
    ATTRIBUTE_K2 = 'k2'
    ATTRIBUTE_K3 = 'k3'
    ATTRIBUTE_K4 = 'k4'

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feComposite')
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

    def setOperator(self, data):
        allowedValues = ['over', 'in', 'out', 'atop', 'xor', 'arithmetic']

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
                self._setNodeAttribute(self.ATTRIBUTE_OPERATOR, data)

    def setK1(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_K1, data)

    def setK2(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_K2, data)

    def setK3(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_K3, data)

    def setK4(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_K4, data)

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

    def getOperator(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_OPERATOR)
        if node != None:
            return node.nodeValue
        return None

    def getK1(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_K1)
        if node != None:
            return node.nodeValue
        return None

    def getK2(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_K2)
        if node != None:
            return node.nodeValue
        return None

    def getK3(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_K3)
        if node != None:
            return node.nodeValue
        return None

    def getK4(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_K4)
        if node != None:
            return node.nodeValue
        return None