from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class AltGlyphItemNode(BasicSvgNode):

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'altGlyphItem')
        