from RGT.XML.SVG.baseStructuralNode import BaseStructuralNode
from RGT.XML.SVG.Attribs.conditionalProcessingAttributes import ConditionalProcessingAttributes
from RGT.XML.SVG.Attribs.positionAttributes import PositionAttributes
from RGT.XML.SVG.Attribs.sizeAttributes import SizeAttributes
from types import StringType
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class UseNode(BaseStructuralNode, PositionAttributes, SizeAttributes, ConditionalProcessingAttributes):
    
    svgNodeType= BasicSvgNode.SVG_USE_NODE
    
    ATTRIBUTE_TRANSFORM= 'transform'
    ATTRIBUTE_XLING_HREF= 'xlink:href'

    def __init__(self, ownerDoc):
        BaseStructuralNode.__init__(self, ownerDoc, 'use')
        PositionAttributes.__init__(self)
        SizeAttributes.__init__(self)
        ConditionalProcessingAttributes.__init__(self)
    
    
    def setTransform(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_TRANSFORM, data)
    
    def setXlinkHref(self, data):
        if data != None:
            if type(data) is not StringType:
                data= str(data)
            self._setNodeAttribute(self.ATTRIBUTE_XLING_HREF, data)
            
     
    def getTransform(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_TRANSFORM)
        if node != None:
            return node.nodeValue
        return None
    
    def getXlinkHref(self):
        node= self._getNodeAttribute(self.ATTRIBUTE_XLING_HREF)
        if node != None:
            return node.nodeValue
        return None