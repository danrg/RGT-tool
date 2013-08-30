from RGT.XML.SVG.baseContainerNode import BaseContainerNode
from RGT.XML.SVG.Attribs.conditionalProcessingAttributes import ConditionalProcessingAttributes
from RGT.XML.SVG.Attribs.graphicalEventAttributes import GraphicalEventAttributes
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class SwitchNode(BaseContainerNode, ConditionalProcessingAttributes, GraphicalEventAttributes):
    svgNodeType = BasicSvgNode.SVG_SWITCH_NODE

    ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED = 'externalResourcesRequired'
    ATTRIBUTE_TRANSFORM = 'transform'

    def __init__(self, ownerDoc):
        BaseContainerNode.__init__(self, ownerDoc, 'switch')
        ConditionalProcessingAttributes.__init__(self)
        GraphicalEventAttributes.__init__(self)
        #add groups
        self._allowedSvgChildNodes.update(self.SVG_GROUP_ANIMATION_ELEMENTS, self.SVG_GROUP_DESCRIPTIVE_ELEMENTS,
                                          self.SVG_GROUP_SHAPE_ELEMENTS)
        #add indivudual elements
        self._allowedSvgChildNodes.update(
            {self.SVG_A_NODE, self.SVG_FOREIGN_OBJECT_NODE, self.SVG_G_NODE, self.SVG_IMAGE_NODE,
             self.SVG_SVG_NODE, self.SVG_SWITCH_NODE, self.SVG_TEXT_NODE, self.SVG_USE_NODE})

    def setExternalResourcesRequired(self, data):
        allowedValues = ['true', 'false']

        if data != None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED, data)

    def setTransform(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TRANSFORM, data)

    def getExternalResourcesRequired(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED)
        if node != None:
            return node.nodeValue
        return None

    def getTransform(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_TRANSFORM)
        if node != None:
            return node.nodeValue
        return None