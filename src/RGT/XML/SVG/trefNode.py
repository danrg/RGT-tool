from RGT.XML.SVG.baseTextNode import BaseTextNode
from RGT.XML.SVG.Attribs.xlinkAttributes import XlinkAttributes

class TrefNode(BaseTextNode, XlinkAttributes):

    def __init__(self, ownerDoc):
        BaseTextNode.__init__(self, ownerDoc, 'tref')
        XlinkAttributes.__init__(self)
        