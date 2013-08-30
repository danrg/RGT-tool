from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class FeTurbulenceNode(BaseFilterNode):
    svgNodeType = BasicSvgNode.SVG_FE_TURBULENCE_NODE

    ATTRIBUTE_BASE_FREQUENCY = 'baseFrequency'
    ATTRIBUTE_NUM_OCTAVES = 'numOctaves'
    ATTRIBUTE_SEED = 'seed'
    ATTRIBUTE_STITCH_TILES = 'stitchTiles'
    ATTRIBUTE_TYPE = 'type'

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feTurbulence')
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_SET_NODE})

    def setBaseFrequency(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_BASE_FREQUENCY, data)

    def setNumOctaves(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_NUM_OCTAVES, data)

    def setSeed(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_SEED, data)

    def setStitchTiles(self, data):
        allowedValues = ['stitch', 'noStitch']

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
                self._setNodeAttribute(self.ATTRIBUTE_STITCH_TILES, data)

    def setType(self, data):
        allowedValues = ['fractalNoise', 'turbulence']

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
                self._setNodeAttribute(self.ATTRIBUTE_TYPE, data)

    def getBaseFrequency(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_BASE_FREQUENCY)
        if node != None:
            return node.nodeValue
        return None

    def getNumOctaves(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_NUM_OCTAVES)
        if node != None:
            return node.nodeValue
        return None

    def getSeed(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_SEED)
        if node != None:
            return node.nodeValue
        return None

    def getStitchTiles(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_STITCH_TILES)
        if node != None:
            return node.nodeValue
        return None

    def getType(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_TYPE)
        if node != None:
            return node.nodeValue
        return None