from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class AltGlyphItemNode(BasicSvgNode):

    svgNodeType= BasicSvgNode.SVG_ALT_GLYPH_ITEM_NODE

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'altGlyphItem')
        self._allowedSvgChildNodes.add(self.SVG_GLYPH_REF_NODE)
        