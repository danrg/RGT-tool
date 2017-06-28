from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.presentationAttributes import PresentationAttributes
from RGT.XML.SVG.Attribs.classAttribute import ClassAttribute
from RGT.XML.SVG.Attribs.styleAttribute import StyleAttribute
from types import StringType


class FontNode(BasicSvgNode):
    svgNodeType = BasicSvgNode.SVG_FONT_NODE

    ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED = 'externalResourcesRequired'
    ATTRIBUTE_HORIZ_ORIGIN_X = 'horiz-origin-x'
    ATTRIBUTE_HORIZ_ORIGIN_Y = 'horiz-origin-y'
    ATTRIBUTE_HORIZ_ADV_X = 'horiz-adv-x'
    ATTRIBUTE_VERT_ORIGIN_X = 'vert-origin-x'
    ATTRIBUTE_VERT_ORIGIN_Y = 'vert-origin-y'
    ATTRIBUTE_VERT_ADV_Y = 'vert-adv-y'

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'font')
        PresentationAttributes.__init__(self)
        ClassAttribute.__init__(self)
        StyleAttribute.__init__(self)
        #add groups
        self._allowedSvgChildNodes.update(self.SVG_GROUP_DESCRIPTIVE_ELEMENTS)
        #add individual nodes
        self._allowedSvgChildNodes.update(
            {self.SVG_FONT_FACE_NODE, self.SVG_GLYPH_NODE, self.SVG_HKERN_NODE, self.SVG_MISSING_GLYPH_NODE,
             self.SVG_VKERN_NODE})

    def setExternalResourcesRequired(self, data):
        allowedValues = ['true', 'false']

        if data is not None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED, data)

    def setHorizOriginX(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_HORIZ_ORIGIN_X, data)

    def setHorizOriginY(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_HORIZ_ORIGIN_Y, data)

    def setHorizAdvX(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_HORIZ_ADV_X, data)

    def setVertOriginX(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VERT_ORIGIN_X, data)

    def setVertOriginY(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VERT_ORIGIN_Y, data)

    def setVertAdvY(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VERT_ADV_Y, data)

    def getExternalResourcesRequired(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED)
        if node is not None:
            return node.nodeValue
        return None

    def getHorizOriginX(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_HORIZ_ORIGIN_X)
        if node is not None:
            return node.nodeValue
        return None

    def getHorizOriginY(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_HORIZ_ORIGIN_Y)
        if node is not None:
            return node.nodeValue
        return None

    def getHorizAdvX(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_HORIZ_ADV_X)
        if node is not None:
            return node.nodeValue
        return None

    def getVertOriginX(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_VERT_ORIGIN_X)
        if node is not None:
            return node.nodeValue
        return None

    def getVertOriginY(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_VERT_ORIGIN_Y)
        if node is not None:
            return node.nodeValue
        return None

    def getVertAdvY(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_VERT_ADV_Y)
        if node is not None:
            return node.nodeValue
        return None