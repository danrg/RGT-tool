from RGT.XML.SVG.baseGlyph import BaseGlyph
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class GlyphNode(BaseGlyph):
    svgNodeType = BasicSvgNode.SVG_GLYPH_NODE

    ATTRIBUTE_UNICODE = 'unicode'
    ATTRIBUTE_GLYPH_NAME = 'glyph-name'
    ATTRIBUTE_ORIENTATION = 'orientation'
    ATTRIBUTE_ARABIC_FORM = 'arabic-form'
    ATTRIBUTE_LANG = 'lang'

    def __init__(self, ownerDoc):
        BaseGlyph.__init__(self, ownerDoc, 'glyph')


    def setUnicode(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_UNICODE, data)

    def setGlyphName(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_GLYPH_NAME, data)

    def setOrientation(self, data):
        allowedValues = ['h', 'v']

        if data != None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_ORIENTATION, data)

    def setArabicForm(self, data):
        allowedValues = ['initial', 'medial', 'terminal', 'isolated']

        if data != None:
            if data not in allowedValues:
                values = ''
                for value in allowedValues:
                    values += value + ', '
                values = values[0: len(values) - 2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_ARABIC_FORM, data)

    def setLang(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_LANG, data)


    def getUnicode(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_UNICODE)
        if node != None:
            return node.nodeValue
        return None

    def getGlyphName(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_GLYPH_NAME)
        if node != None:
            return node.nodeValue
        return None

    def getOrientation(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ORIENTATION)
        if node != None:
            return node.nodeValue
        return None

    def getArabicForm(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ARABIC_FORM)
        if node != None:
            return node.nodeValue
        return None

    def getLang(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_LANG)
        if node != None:
            return node.nodeValue
        return None