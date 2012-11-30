from RGT.XML.SVG.structuralNode import StructuralNode
from types import StringType

class SymbolNode(StructuralNode):
    
    ATTRIBUTE_PRESERVEASPECTRATIO= 'preserveAspectRatio'
    ATTRIBUTE_VIEWBOX= 'viewBox'


    def __init__(self, ownderDoc):
        StructuralNode.__init__(self, ownderDoc)
        
    
    def setPreserveAspectRatio(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_PRESERVEASPECTRATIO, data)
            
    def setViewBox(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_VIEWBOX, data)
    
    def getViewBox(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_VIEWBOX)
        if node != None:
            return node.nodeValue
        return None
    
    def getPreserveAspectRatio(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_PRESERVEASPECTRATIO)
        if node != None:
            return node.nodeValue
        return None