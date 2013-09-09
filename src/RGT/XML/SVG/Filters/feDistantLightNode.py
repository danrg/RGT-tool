from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from types import StringType


class FeDistantLightNode(BasicSvgNode):
    svgNodeType = BasicSvgNode.SVG_FE_DISTANT_LIGHT_NODE

    ATTRIBUTE_AZIMUTH = 'azimuth'
    ATTRIBUTE_ELEVATION = 'elevation'

    def __init__(self, ownerDoc, azimuth=None, elevation=None):
        BasicSvgNode.__init__(self, ownerDoc, 'feDistantLight')
        self.setAzimuth(azimuth)
        self.setElevation(elevation)
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_SET_NODE})

    def setAzimuth(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_AZIMUTH, data)

    def setElevation(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ELEVATION, data)

    def getAzimuth(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_AZIMUTH)
        if node != None:
            return node.nodeValue
        return None

    def getElevation(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ELEVATION)
        if node != None:
            return node.nodeValue
        return None    