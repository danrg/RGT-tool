from RGT.XML.SVG.basePolyNode import BasePolyNode

class PolylineNode(BasePolyNode):

    def __init__(self, ownerDoc):
        BasePolyNode.__init__(self, ownerDoc, 'polyline')
        