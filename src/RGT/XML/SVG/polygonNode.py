from RGT.XML.SVG.basePolyNode import BasePolyNode

class Polygon(BasePolyNode):

    def __init__(self, ownerDoc):
        BasePolyNode.__init__(self, ownerDoc, 'polygon')
        