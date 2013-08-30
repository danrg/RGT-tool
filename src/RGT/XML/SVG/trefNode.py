from RGT.XML.SVG.baseTextNode import BaseTextNode
from RGT.XML.SVG.Attribs.xlinkAttributes import XlinkAttributes
from RGT.XML.SVG.basicSvgNode import BasicSvgNode


class TrefNode(BaseTextNode, XlinkAttributes):
    svgNodeType = BasicSvgNode.SVG_TREF_NODE

    def __init__(self, ownerDoc):
        BaseTextNode.__init__(self, ownerDoc, 'tref')
        XlinkAttributes.__init__(self)
        self._allowedSvgChildNodes.update({self.SVG_ANIMATE_NODE, self.SVG_ANIMATE_COLOR_NODE, self.SVG_SET_NODE})