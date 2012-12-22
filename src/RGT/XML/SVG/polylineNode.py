from RGT.XML.SVG.basePolyNode import BasePolyNode

class PolylineNode(BasePolyNode):

    def __init__(self, ownerDoc, points= None):
        BasePolyNode.__init__(self, ownerDoc, 'polyline')
        self.setPoints(points)
        