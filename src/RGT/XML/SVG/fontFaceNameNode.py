from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from types import StringType

class FontFaceNameNode(BasicSvgNode):
    
    ATTRIBUTE_NAME= 'name'

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'font-face-name')
    
    
    def setName(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_NAME, data)
    
    def getName(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_NAME)
        if node != None:
            return node.nodeValue
        return None