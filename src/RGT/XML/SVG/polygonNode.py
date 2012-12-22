from RGT.XML.SVG.basePolyNode import BasePolyNode

class PolygonNode(BasePolyNode):

    def __init__(self, ownerDoc, points= None):
        BasePolyNode.__init__(self, ownerDoc, 'polygon')
        self.setPoints(points)
        