from RGT.XML.SVG.Filters.baseFilterNode import BaseFilterNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class FeDiffuseLightingNode(BaseFilterNode):
    svgNodeType = BasicSvgNode.SVG_FE_DIFFUSE_LIGHTING_NODE

    ATTRIBUTE_IN = 'in'
    ATTRIBUTE_SURFACE_SCALE = 'surfaceScale'
    ATTRIBUTE_DIFFUSE_CONSTANT = 'diffuseConstant'
    ATTRIBUTE_KERNEL_UNIT_LENGTH = 'kernelUnitLength'

    def __init__(self, ownerDoc):
        BaseFilterNode.__init__(self, ownerDoc, 'feDiffuseLighting')
        self._allowedSvgChildNodes.update(self.SVG_GROUP_DESCRIPTIVE_ELEMENTS, self.SVG_GROUP_LIGHT_SOURCE_ELEMENTS)

    def setIn(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IN, data)

    def setSurfaceScale(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_SURFACE_SCALE, data)

    def setDiffuseConstant(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_DIFFUSE_CONSTANT, data)

    def setKernelUnitLength(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_KERNEL_UNIT_LENGTH, data)

    def getIn(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_IN)
        if node != None:
            return node.nodeValue
        return None

    def getSurfaceScale(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_SURFACE_SCALE)
        if node != None:
            return node.nodeValue
        return None

    def getDiffuseConstant(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_DIFFUSE_CONSTANT)
        if node != None:
            return node.nodeValue
        return None

    def getKernelUnitLength(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_KERNEL_UNIT_LENGTH)
        if node != None:
            return node.nodeValue
        return None