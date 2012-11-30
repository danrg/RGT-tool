from RGT.XML.SVG.Attribs.basicSvgAttribute import BasicSvgAttribute
from types import StringType

class StyleAttribute(BasicSvgAttribute):

    ATTRIBUTE_STYLE= 'style'

    def setStyle(self, data= None):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STYLE, data)
            
    def geStyle(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_STYLE)
        if node != None:
            return node.nodeValue
        return None
    
    