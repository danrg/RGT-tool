from RGT.XML.SVG.basicSvgNode import BasicSvgNode

class FontFaceSrcNode(BasicSvgNode):

    svgNodeType= BasicSvgNode.SVG_FONT_FACE_SRC_NODE

    def __init__(self, ownerDoc):
        BasicSvgNode.__init__(self, ownerDoc, 'font-face-src')
        