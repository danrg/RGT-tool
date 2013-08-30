from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from RGT.XML.SVG.Attribs.positionAttributes import PositionAttributes
from RGT.XML.SVG.Attribs.sizeAttributes import SizeAttributes
from types import StringType


class FilterPrimitiveAttributes(PositionAttributes, SizeAttributes, BasicSvgAttribute):
    ATTRIBUTE_RESULT = 'result'

    def __init__(self):
        BasicSvgAttribute.__init__(self)
        PositionAttributes.__init__(self)
        SizeAttributes.__init__(self)


    def setResult(self, data=None):
        if data != None:
            if type(data) is not StringType:
                data = str(data)
            self._setNodeAttribute(self.ATTRIBUTE_RESULT, data)

    def geResult(self):
        node = self._getNodeAttribute(self.ATTRIBUTE_RESULT)
        if node != None:
            return node.nodeValue
        return None
    