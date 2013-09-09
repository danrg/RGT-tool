from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from types import StringType


class FontFaceNode(BasicSvgNode):
    svgNodeType = BasicSvgNode.SVG_FONT_FACE_NODE

    ATTRIBUTE_FONT_FAMILY = 'font-family'
    ATTRIBUTE_FONT_SIZE = 'font-size'
    ATTRIBUTE_FONT_STRETCH = 'font-stretch'
    ATTRIBUTE_FONT_STYLE = 'font-style'
    ATTRIBUTE_FONT_VARIANT = 'font-variant'
    ATTRIBUTE_FONT_WEIGHT = 'font-weight'
    ATTRIBUTE_UNICODE_RANGE = 'unicade-range'
    ATTRIBUTE_UNITS_PER_EM = 'units-per-em'
    ATTRIBUTE_PANOSE_1 = 'panose-1'
    ATTRIBUTE_STEMV = 'stemv'
    ATTRIBUTE_STEMH = 'stemh'
    ATTRIBUTE_SLOPE = 'slope'

    #2nd div
    ATTRIBUTE_CAP_HEIGHT = 'cap-height'
    ATTRIBUTE_X_HEIGHT = 'x-height'
    ATTRIBUTE_ACCENT_HEIGHT = 'accent-height'
    ATTRIBUTE_ASCENT = 'ascent'
    ATTRIBUTE_DESCENT = 'descent'
    ATTRIBUTE_WIDTHS = 'widths'
    ATTRIBUTE_BBOX = 'bbox'
    ATTRIBUTE_IDEOGRAPHIC = 'ideographic'
    ATTRIBUTE_ALPHABETIC = 'alphabetic'
    ATTRIBUTE_MATHEMATICAL = 'mathematical'
    ATTRIBUTE_HANGING = 'hanging'
    ATTRIBUTE_V_IDEOGRAPHIC = 'v-ideographic'

    #3rd div
    ATTRIBUTE_V_ALPHABETIC = 'v-alphabetic'
    ATTRIBUTE_V_MATHEMATICAL = 'v-mathematical'
    ATTRIBUTE_V_HANGING = 'v-hanging'
    ATTRIBUTE_UNDERLINE_POSITION = 'underline-position'
    ATTRIBUTE_UNDERLINE_THICKNESS = 'underline-thickness'
    ATTRIBUTE_STRIKETHROUGH_POSITION = 'strikethrough-position'
    ATTRIBUTE_STRIKETHROUGH_THICKNESS = 'strikethrough-thickness'
    ATTRIBUTE_OVERLINE_POSITION = 'overline-position'
    ATTRIBUTE_OVERLINE_THICKNESS = 'overline-thickness'

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'font-face')
        #add groups
        self._allowedSvgChildNodes.update(self.SVG_GROUP_DESCRIPTIVE_ELEMENTS)
        #add individual nodes
        self._allowedSvgChildNodes.add(self.SVG_FONT_FACE_SRC_NODE)

    def setFontFamily(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FONT_FAMILY, data)

    def setFontSize(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FONT_SIZE, data)

    def setFontStretch(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FONT_STRETCH, data)

    def setFontStyle(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FONT_STYLE, data)

    def setFontVariant(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FONT_VARIANT, data)

    def setFontWeight(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_FONT_WEIGHT, data)

    def setUnicodeRange(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_UNICODE_RANGE, data)

    def setUnitsPerEm(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_UNITS_PER_EM, data)

    def setPanose1(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_PANOSE_1, data)

    def setStemV(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STEMV, data)

    def setStemH(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STEMH, data)

    def setSlope(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_SLOPE, data)

    #2nd div

    def setCapHeight(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_CAP_HEIGHT, data)

    def setXHeight(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_X_HEIGHT, data)

    def setAccentHeight(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ACCENT_HEIGHT, data)

    def setAscent(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ASCENT, data)

    def setDescent(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_DESCENT, data)

    def setWidths(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_WIDTHS, data)

    def setBBox(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_BBOX, data)

    def setIdeographic(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_IDEOGRAPHIC, data)

    def setAlphabetic(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_ALPHABETIC, data)

    def setMathematical(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_MATHEMATICAL, data)

    def setHanging(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_HANGING, data)

    def setVIdeographic(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_V_IDEOGRAPHIC, data)

    #3rd div

    def setVAlphabetic(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_V_ALPHABETIC, data)

    def setVMathematical(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_V_MATHEMATICAL, data)

    def setVHanging(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_V_HANGING, data)

    def setUnderlinePosition(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_UNDERLINE_POSITION, data)

    def setUnderlineThickness(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_UNDERLINE_THICKNESS, data)

    def setStrikeThroughPosition(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STRIKETHROUGH_POSITION, data)

    def setStrikeThroughThickness(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STRIKETHROUGH_THICKNESS, data)

    def setOverlinePosition(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_OVERLINE_POSITION, data)

    def setOverlineThickness(self, data):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_OVERLINE_THICKNESS, data)

    #gets

    def getFontFamily(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_FONT_FAMILY)
        if node != None:
            return node.nodeValue
        return None

    def getFontSize(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_FONT_SIZE)
        if node != None:
            return node.nodeValue
        return None

    def getFontStretch(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_FONT_STRETCH)
        if node != None:
            return node.nodeValue
        return None

    def getFontStyle(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_FONT_STYLE)
        if node != None:
            return node.nodeValue
        return None

    def getFontVariant(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_FONT_VARIANT)
        if node != None:
            return node.nodeValue
        return None

    def getFontWeight(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_FONT_WEIGHT)
        if node != None:
            return node.nodeValue
        return None

    def getUnicodeRange(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_UNICODE_RANGE)
        if node != None:
            return node.nodeValue
        return None

    def getUnitsPerEm(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_UNITS_PER_EM)
        if node != None:
            return node.nodeValue
        return None

    def getPanose1(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_PANOSE_1)
        if node != None:
            return node.nodeValue
        return None

    def getStemv(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_STEMV)
        if node != None:
            return node.nodeValue
        return None

    def getStemh(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_STEMH)
        if node != None:
            return node.nodeValue
        return None

    def getSlope(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_SLOPE)
        if node != None:
            return node.nodeValue
        return None

    #2nd div

    def getCapHeight(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_CAP_HEIGHT)
        if node != None:
            return node.nodeValue
        return None

    def getXHeight(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_X_HEIGHT)
        if node != None:
            return node.nodeValue
        return None

    def getAccentHeight(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ACCENT_HEIGHT)
        if node != None:
            return node.nodeValue
        return None

    def getAscent(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ASCENT)
        if node != None:
            return node.nodeValue
        return None

    def getDescent(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_DESCENT)
        if node != None:
            return node.nodeValue
        return None

    def getWidths(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_WIDTHS)
        if node != None:
            return node.nodeValue
        return None

    def getBBox(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_BBOX)
        if node != None:
            return node.nodeValue
        return None

    def getIdeographic(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_IDEOGRAPHIC)
        if node != None:
            return node.nodeValue
        return None

    def getAlphabetic(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_ALPHABETIC)
        if node != None:
            return node.nodeValue
        return None

    def getMathematical(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_MATHEMATICAL)
        if node != None:
            return node.nodeValue
        return None

    def getHanging(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_HANGING)
        if node != None:
            return node.nodeValue
        return None

    def getVIdeographic(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_V_IDEOGRAPHIC)
        if node != None:
            return node.nodeValue
        return None

    #3rd div

    def getVAlphabetic(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_V_ALPHABETIC)
        if node != None:
            return node.nodeValue
        return None

    def getVMathematical(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_V_MATHEMATICAL)
        if node != None:
            return node.nodeValue
        return None

    def getVHanging(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_V_HANGING)
        if node != None:
            return node.nodeValue
        return None

    def getUnderlinePosition(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_UNDERLINE_POSITION)
        if node != None:
            return node.nodeValue
        return None

    def getUnderlineThickness(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_UNDERLINE_THICKNESS)
        if node != None:
            return node.nodeValue
        return None

    def getStrikethroughPosition(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_STRIKETHROUGH_POSITION)
        if node != None:
            return node.nodeValue
        return None

    def getStrikethroughThickness(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_STRIKETHROUGH_THICKNESS)
        if node != None:
            return node.nodeValue
        return None

    def getOverlinePosition(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_OVERLINE_POSITION)
        if node != None:
            return node.nodeValue
        return None

    def getOverlineThickness(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_OVERLINE_THICKNESS)
        if node != None:
            return node.nodeValue
        return None