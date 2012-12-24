from RGT.XML.SVG.baseStructuralNode import BaseStructuralNode
from RGT.XML.SVG.Attribs.conditionalProcessingAttributes import ConditionalProcessingAttributes
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class GNode(BaseStructuralNode, ConditionalProcessingAttributes):
    
    svgNodeType= BasicSvgNode.SVG_G_NODE
    
    ATTRIBUTE_TRANSFORM= 'transform'
    
    
    def __init__(self, ownerDoc):
        BaseStructuralNode.__init__(self, ownerDoc, 'g')
        ConditionalProcessingAttributes.__init__(self)
        
    
    def setTransform(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TRANSFORM, data)
            
     
    def getTransform(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_TRANSFORM)
        if node != None:
            return node.nodeValue
        return None