from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from types import StringType

class FontFaceFormatNode(BasicSvgNode):
   
    svgNodeType= BasicSvgNode.SVG_FONT_FACE_FORMAT_NODE
   
    ATTRIBUTE_STRING= 'string'

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'font-face-format')
        
    
    def setString(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_STRING, data)
    
    def getString(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_STRING)
        if node != None:
            return node.nodeValue
        return None
        