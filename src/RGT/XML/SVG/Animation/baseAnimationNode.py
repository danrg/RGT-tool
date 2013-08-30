from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.conditionalProcessingAttributes import ConditionalProcessingAttributes
from RGT.XML.SVG.Attribs.xlinkAttributes import XlinkAttributes
from RGT.XML.SVG.Attribs.animationTimingAttributes import AnimationTimingAttributes


class BaseAnimationNode(BasicSvgNode):
    ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED = 'externalResourcesRequired'


    def __init__(self, ownerDoc, tagName):
        BasicSvgNode.__init__(self, ownerDoc, tagName)
        ConditionalProcessingAttributes.__init__(self)
        XlinkAttributes.__init__(self)
        AnimationTimingAttributes.__init__(self)
        self._allowedSvgChildNodes.update(self.SVG_GROUP_DESCRIPTIVE_ELEMENTS)

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

    def getExternalResourcesRequired(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED)
        if node != None:
            return node.nodeValue
        return None
        