from RGT.XML.SVG.basePolyNode import BasePolyNode
from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class PolygonNode(BasePolyNode):

    svgNodeType= BasicSvgNode.SVG_POLYGON_NODE

    def __init__(self, ownerDoc, points= None):
        BasePolyNode.__init__(self, ownerDoc, 'polygon')
        self.setPoints(points)
        