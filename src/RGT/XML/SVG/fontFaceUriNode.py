from RGT.XML.SVG.basicSvgNode import BasicSvgNode
from RGT.XML.SVG.Attribs.xlinkAttributes import XlinkAttributes


class FontFaceUriNode(BasicSvgNode, XlinkAttributes):
    
    svgNodeType= BasicSvgNode.SVG_FONT_FACE_URI_NODE
    
    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'font-face-uri')
        XlinkAttributes.__init__(self)