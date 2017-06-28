from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute


class AnimationAdditionAttributes(BasicSvgAttribute):
    ATTRIBUTE_ADDITIVE = 'additive'
    ATTRIBUTE_ACCUMULATE = 'accumulate'


    def __init__(self):
        BasicSvgAttribute.__init__(self)

    def setAdditive(self, data):
        allowedValues = ['replace', 'sum']

        if data is not None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_ADDITIVE, data)

    def setAccumulate(self, data):
        allowedValues = ['none', 'sum']

        if data is not None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_ACCUMULATE, data)

    def getAddtive(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ADDITIVE)
        if node is not None:
            return node.nodeValue
        return None

    def getAccumulate(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ACCUMULATE)
        if node is not None:
            return node.nodeValue
        return None
        