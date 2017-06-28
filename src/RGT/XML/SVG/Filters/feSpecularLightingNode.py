from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class FeSpecularLightingNode(BaseFilterNode):
    svgNodeType = BasicSvgNode.SVG_FE_SPECULAR_LIGHTING_NODE

    ATTRIBUTE_IN = 'in'
    ATTRIBUTE_SURFACE_SCALE = 'surfaceScale'
    ATTRIBUTE_SPECULAR_CONSTANT = 'specularConstant'
    ATTRIBUTE_SPECULAR_EXPONENT = 'specularExponent'
    ATTRIBUTE_KERNEL_UNIT_LENGTH = 'kernelUnitLength'

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feSpecularLighting')
        self._allowedSvgChildNodes.update(self.SVG_GROUP_DESCRIPTIVE_ELEMENTS, self.SVG_GROUP_LIGHT_SOURCE_ELEMENTS)


    def setIn(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IN, data)

    def setSurfaceScale(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_SURFACE_SCALE, data)

    def setSpecularConstant(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_SPECULAR_CONSTANT, data)

    def setSpecularExponent(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_SPECULAR_EXPONENT, data)

    def setKernelUnitLength(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_KERNEL_UNIT_LENGTH, data)

    def getIn(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_IN)
        if node is not None:
            return node.nodeValue
        return None

    def getSurfaceScale(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_SURFACE_SCALE)
        if node is not None:
            return node.nodeValue
        return None

    def getSpecularConstant(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_SPECULAR_CONSTANT)
        if node is not None:
            return node.nodeValue
        return None

    def getSpecularExponent(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_SPECULAR_EXPONENT)
        if node is not None:
            return node.nodeValue
        return None

    def getKernelUnitLength(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_KERNEL_UNIT_LENGTH)
        if node is not None:
            return node.nodeValue
        return None