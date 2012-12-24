from RGT.XML.SVG.basePolyNode import BasePolyNode
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class PolylineNode(BasePolyNode):

    svgNodeType= BasicSvgNode.SVG_POLYLINE_NODE

    def __init__(self, ownerDoc, points= None):
        BasePolyNode.__init__(self, ownerDoc, 'polyline')
        self.setPoints(points)
        