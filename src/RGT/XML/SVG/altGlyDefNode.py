from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class AltGlyphDefNode(BasicSvgNode):

    svgNodeType= BasicSvgNode.SVG_ALT_GLYPH_DEF_NODE

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'altGlyphDef')
        