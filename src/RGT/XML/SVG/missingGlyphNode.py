from RGT.XML.SVG.baseGlyph import BaseGlyph

class MissingGlyph(BaseGlyph):

    def __init__(self, ownerDoc):
        BaseGlyph.__init__(self, ownerDoc, 'missing-glyph')
        