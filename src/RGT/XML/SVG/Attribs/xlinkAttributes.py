from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType


class XlinkAttributes(BasicSvgAttribute):
    ATTRIBUTE_XLINK_HREF = 'xlink:href'
    ATTRIBUTE_XLINK_SHOW = 'xlink:show'
    ATTRIBUTE_XLINK_ACTUATE = 'xlink:actuate'
    ATTRIBUTE_XLINK_TYPE = 'xlink:type'
    ATTRIBUTE_XLINK_ROLE = 'xlink:role'
    ATTRIBUTE_XLINK_ARCROLE = 'xlink:arcrole'
    ATTRIBUTE_XLINK_TITLE = 'xlink:title'

    def __init__(self):
        BasicSvgAttribute.__init__(self)


    def setXlinkHref(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_XLINK_HREF, data)

    def setXlinkShow(self, data):
        allowedValues = ['new', 'replace', 'embed', 'other', 'none']

        if data is not None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_XLINK_SHOW, data)

    def setXlinkActuate(self, data):
        allowedValues = ['onLoad']

        if data is not None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_XLINK_ACTUATE, data)

    def setXlinkType(self, data):
        allowedValues = ['simple']

        if data is not None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_XLINK_TYPE, data)

    def setXlinkRole(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_XLINK_ROLE, data)

    def setXlinkArcrole(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_XLINK_ARCROLE, data)

    def setXlinkTitle(self, data):
        if data is not None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_XLINK_TITLE, data)

    def getXlinkHref(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_XLINK_HREF)
        if node is not None:
            return node.nodeValue
        return None

    def getXlinkShow(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_XLINK_SHOW)
        if node is not None:
            return node.nodeValue
        return None

    def getXlinkActuate(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_XLINK_ACTUATE)
        if node is not None:
            return node.nodeValue
        return None

    def getXlinkType(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_XLINK_TYPE)
        if node is not None:
            return node.nodeValue
        return None

    def getXlinkRole(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_XLINK_ROLE)
        if node is not None:
            return node.nodeValue
        return None

    def getXlinkArcrole(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_XLINK_ARCROLE)
        if node is not None:
            return node.nodeValue
        return None

    def getXlinkTitle(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_XLINK_TITLE)
        if node is not None:
            return node.nodeValue
        return None