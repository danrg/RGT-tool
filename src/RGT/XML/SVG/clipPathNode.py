from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.conditionalProcessingAttributes import ConditionalProcessingAttributes
from RGT.XML.SVG.Attribs.presentationAttributes import PresentationAttributes
from RGT.XML.SVG.Attribs.classAttribute import ClassAttribute
from RGT.XML.SVG.Attribs.styleAttribute import StyleAttribute
from types import StringType


class ClipPathNode(BasicSvgNode, ConditionalProcessingAttributes, PresentationAttributes, ClassAttribute,
                   StyleAttribute):
    svgNodeType = BasicSvgNode.SVG_CLIP_PATH_NODE

    ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED = 'externalResourcesRequired'
    ATTRIBUTE_TRANSFORM = 'transform'
    ATTRIBUTE_CLIP_PATH_UNITS = 'clipPathUnits'

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'clipPath')
        ConditionalProcessingAttributes.__init__(self)
        PresentationAttributes.__init__(self)
        ClassAttribute.__init__(self)
        StyleAttribute.__init__(self)
        #add groups
        self._allowedSvgChildNodes.update(self.SVG_GROUP_ANIMATION_ELEMENTS, self.SVG_GROUP_DESCRIPTIVE_ELEMENTS,
                                          self.SVG_GROUP_SHAPE_ELEMENTS)
        #ad individual nodes
        self._allowedSvgChildNodes.update({self.SVG_TEXT_NODE, self.SVG_USE_NODE})

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

    def setTransform(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TRANSFORM, data)

    def setClipPathUnits(self, data):
        allowedValues = ['userSpaceOnUse', 'objectBoundingBox']

        if data is not None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_CLIP_PATH_UNITS, data)

    def getExternalResourcesRequired(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED)
        if node is not None:
            return node.nodeValue
        return None

    def getTransform(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_TRANSFORM)
        if node is not None:
            return node.nodeValue
        return None

    def getClipPathUnits(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_CLIP_PATH_UNITS)
        if node is not None:
            return node.nodeValue
        return None