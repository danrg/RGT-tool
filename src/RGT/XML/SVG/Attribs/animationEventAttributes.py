from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType


class AnimationEventAttributes(BasicSvgAttribute):
    ATTRIBUTE_ONBEGIN = 'onbegin'
    ATTRIBUTE_ONEND = 'onend'
    ATTRIBUTE_ONREPEAT = 'onrepeat'
    ATTRIBUTE_ONLOAD = 'onload'

    def __init__(self):
        BasicSvgAttribute.__init__(self)

    def setOnbegin(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ONBEGIN, data)

    def setOnend(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ONEND, data)

    def setOnrepeat(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ONREPEAT, data)

    def setOnload(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ONLOAD, data)

    def getOnbegin(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ONBEGIN)
        if node != None:
            return node.nodeValue
        return None

    def getOnend(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ONEND)
        if node != None:
            return node.nodeValue
        return None

    def getRepeat(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ONREPEAT)
        if node != None:
            return node.nodeValue
        return None

    def getOnload(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ONLOAD)
        if node != None:
            return node.nodeValue
        return None
        