from RGT.XML.SVG.baseScriptNode import BaseScriptNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class StyleNode(BaseScriptNode):
    svgNodeType = BasicSvgNode.SVG_STYLE_NODE

    ATTRIBUTE_TYPE = 'type'
    ATTRIBUTE_MEDIA = 'media'
    ATTRIBUTE_TITLE = 'title'


    def __init__(self, ownerDoc):
        BaseScriptNode.__init__(self, ownerDoc, 'style')

    def setType(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TYPE, data)

    def setMedia(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_MEDIA, data)

    def setTitle(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TITLE, data)

    def getType(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_TYPE)
        if node is not None:
            return node.nodeValue
        return None

    def getMedia(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_MEDIA)
        if node is not None:
            return node.nodeValue
        return None

    def getTitle(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_TITLE)
        if node is not None:
            return node.nodeValue
        return None