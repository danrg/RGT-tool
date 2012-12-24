from RGT.XML.SVG.baseStructuralNode import BaseStructuralNode
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class SymbolNode(BaseStructuralNode):
    
    svgNodeType= BasicSvgNode.SVG_SYMBOL_NODE
    
    ATTRIBUTE_PRESERVEASPECTRATIO= 'preserveAspectRatio'
    ATTRIBUTE_VIEWBOX= 'viewBox'


    def __init__(self, ownderDoc):
        BaseStructuralNode.__init__(self, ownderDoc, 'symbol')
        
    
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