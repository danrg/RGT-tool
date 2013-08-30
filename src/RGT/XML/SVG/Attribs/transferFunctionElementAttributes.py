from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType


class TransferFunctionElementAttributes(BasicSvgAttribute):
    ATTRIBUTE_TYPE = 'type'
    ATTRIBUTE_TABLE_VALUES = 'tableValues'
    ATTRIBUTE_SLOPE = 'slope'
    ATTRIBUTE_INTERCEPT = 'intercept'
    ATTRIBUTE_AMPLITUDE = 'amplitude'
    ATTRIBUTE_EXPONENT = 'exponent'
    ATTRIBUTE_OFFSET = 'offset'

    def __init__(self):
        BasicSvgAttribute.__init__(self)

    def setType(self, data):
        allowedValues = ['identity', 'table', 'discrete', 'linear', 'gamma']

        if data != None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_TYPE, data)

    def setTableValues(self, data=None):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TABLE_VALUES, data)

    def setSlope(self, data=None):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_SLOPE, data)

    def setIntercept(self, data=None):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_INTERCEPT, data)

    def setAmplitude(self, data=None):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_AMPLITUDE, data)

    def setExponent(self, data=None):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_EXPONENT, data)

    def setOffset(self, data=None):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_OFFSET, data)

    def getType(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_TYPE)
        if node != None:
            return node.nodeValue
        return None

    def getTableValues(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_TABLE_VALUES)
        if node != None:
            return node.nodeValue
        return None

    def getSlope(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_SLOPE)
        if node != None:
            return node.nodeValue
        return None

    def getIntercept(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_INTERCEPT)
        if node != None:
            return node.nodeValue
        return None

    def getAmplitude(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_AMPLITUDE)
        if node != None:
            return node.nodeValue
        return None

    def getExponent(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_EXPONENT)
        if node != None:
            return node.nodeValue
        return None

    def getOffset(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_OFFSET)
        if node != None:
            return node.nodeValue
        return None