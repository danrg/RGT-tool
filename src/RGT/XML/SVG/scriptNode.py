from RGT.XML.SVG.baseScriptNode import BaseScriptNode
from RGT.XML.SVG.Attribs.xlinkAttributes import XlinkAttributes
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class ScriptNode(BaseScriptNode, XlinkAttributes):
    svgNodeType = BasicSvgNode.SVG_SCRIPT_NODE

    ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED = 'externalResourcesRequired'
    ATTRIBUTE_TYPE = 'type'

    def __init__(self, ownerDoc):
        BaseScriptNode.__init__(self, ownerDoc, 'script')
        XlinkAttributes.__init__(self)

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

    def setType(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TYPE, data)

    def getExternalResourcesRequired(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_EXTERNAL_RESOURCES_REQUIRED)
        if node != None:
            return node.nodeValue
        return None

    def getType(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_TYPE)
        if node != None:
            return node.nodeValue
        return None  