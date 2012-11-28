from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.conditionalProcessingAttributes import ConditionalProcessingAttributes
from RGT.XML.SVG.Attribs.graphicalEventAttributes import GraphicalEventAttributes

class GraphicNode(BasicSvgNode, ConditionalProcessingAttributes, GraphicalEventAttributes):
    
    def __init__(self, ownerDoc, tagName):
        BasicSvgNode.__init__(self, ownerDoc, tagName)
    
    def setStyle(self, cssCode):
        self._setNodeAttribute('style', cssCode)   

        