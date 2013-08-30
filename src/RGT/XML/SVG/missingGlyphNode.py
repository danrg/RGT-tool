from RGT.XML.SVG.baseGlyph import BaseGlyph
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class MissingGlyph(BaseGlyph):
    svgNodeType = BasicSvgNode.SVG_MISSING_GLYPH_NODE

    def __init__(self, ownerDoc):
        BaseGlyph.__init__(self, ownerDoc, 'missing-glyph')
        