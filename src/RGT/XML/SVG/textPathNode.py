from RGT.XML.SVG.baseEditableTextNode import BaseEditableTextNode
from RGT.XML.SVG.Attribs.xlinkAttributes import XlinkAttributes
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class TextPathNode(BaseEditableTextNode, XlinkAttributes):

    svgNodeType= BasicSvgNode.SVG_TEX_PATH_NODE
    
    ATTRIBUTE_START_OFFSET= 'startOffset'
    ATTRIBUTE_METHOD= 'method'
    ATTRIBUTE_SPACING= 'spacing'

    def __init__(self, ownerDoc):
        BaseEditableTextNode.__init__(self, ownerDoc, 'textPath')
        XlinkAttributes.__init__(self)
        self._allowedSvgChildNodes.update({self.SVG_A_NODE, self.SVG_ALT_GLYPH_NODE, self.SVG_ANIMATE_NODE, self.SVG_ANIMATE_COLOR_NODE,
                                           self.SVG_SET_NODE, self.SVG_TREF_NODE, self.SVG_TSPAN_NODE})
    
    def setStartOffset(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_START_OFFSET, data)
    
    def setMethod(self, data):
        allowedValues= ['align', 'stretch']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_METHOD, data)
    
    def setSpacing(self, data):
        allowedValues= ['auto', 'exact']
        
        if data != None:
            if data not in allowedValues:
                values= ''
                for value in allowedValues:
                    values+= value + ', '
                values= values[0: len(values)-2]
                raise ValueError('Value not allowed, only ' + values + 'are allowed')
            else:
                self._setNodeAttribute(self.ATTRIBUTE_SPACING, data)
    
    def getStartOffset(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_START_OFFSET)
        if node != None:
            return node.nodeValue
        return None
        
    def getMethod(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_METHOD)
        if node != None:
            return node.nodeValue
        return None
    
    def getSpacing(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_SPACING)
        if node != None:
            return node.nodeValue
        return None