from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class FeConvolveMatrixNode(BaseFilterNode):
    svgNodeType = BasicSvgNode.SVG_FE_CONVOLVE_MATRIX_NODE

    ATTRIBUTE_IN = 'in'
    ATTRIBUTE_ORDER = 'order'
    ATTRIBUTE_KERNEL_MATRIX = 'kernelMatrix'
    ATTRIBUTE_DIVISOR = 'divisor'
    ATTRIBUTE_BIAS = 'bias'
    ATTRIBUTE_TARGER_X = 'targetX'
    ATTRIBUTE_TARGET_Y = 'targetY'
    ATTRIBUTE_EDGE_MODE = 'edgeMode'
    ATTRIBUTE_KERNEL_UNIT_LENGTH = 'kernelUnitLength'
    ATTRIBUTE_PRESERVE_ALPHA = 'preserveAlpha'

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feConvolveMatrix')
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_SET_NODE})

    def setIn(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IN, data)

    def setOrder(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ORDER, data)

    def setKernelMatrix(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_KERNEL_MATRIX, data)

    def setDivisor(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_DIVISOR, data)

    def setBias(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_BIAS, data)

    def setTargetX(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TARGER_X, data)

    def setTargeY(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TARGET_Y, data)

    def setEdgeMode(self, data):
        allowedValues = ['duplicate', 'wrap', 'none']

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
                self._setNodeAttribute(self.ATTRIBUTE_EDGE_MODE, data)

    def setKernelUnitLength(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_KERNEL_UNIT_LENGTH, data)

    def setPreserveAlpha(self, data):
        allowedValues = ['true', 'false']

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
                self._setNodeAttribute(self.ATTRIBUTE_PRESERVE_ALPHA, data)

    def getIn(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_IN)
        if node is not None:
            return node.nodeValue
        return None

    def getOrder(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ORDER)
        if node is not None:
            return node.nodeValue
        return None

    def getKernelMatrix(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_KERNEL_MATRIX)
        if node is not None:
            return node.nodeValue
        return None

    def getDivisor(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_DIVISOR)
        if node is not None:
            return node.nodeValue
        return None

    def getBias(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_BIAS)
        if node is not None:
            return node.nodeValue
        return None

    def getTargetX(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_TARGER_X)
        if node is not None:
            return node.nodeValue
        return None

    def getTargetY(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_TARGET_Y)
        if node is not None:
            return node.nodeValue
        return None

    def getEdgeMode(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_EDGE_MODE)
        if node is not None:
            return node.nodeValue
        return None

    def getKernelUnitLength(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_KERNEL_UNIT_LENGTH)
        if node is not None:
            return node.nodeValue
        return None

    def getPreserveAlpha(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_PRESERVE_ALPHA)
        if node is not None:
            return node.nodeValue
        return None